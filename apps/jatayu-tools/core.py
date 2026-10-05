"""Local conversion engine. No sockets or external service calls."""
from __future__ import annotations

import io
import math
import os
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageOps, ImageSequence, UnidentifiedImageError
from pypdf import PdfReader, PdfWriter

IMAGE_INPUT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff", ".gif"}
IMAGE_OUTPUT = {"PNG": ".png", "JPG": ".jpg", "JPEG": ".jpg", "WEBP": ".webp", "BMP": ".bmp", "TIFF": ".tiff", "PDF": ".pdf"}
PDF_PRESETS = {"Screen (small)": "/screen", "Ebook": "/ebook", "Printer": "/printer", "Prepress": "/prepress"}
MAX_PIXELS = 180_000_000
Image.MAX_IMAGE_PIXELS = MAX_PIXELS


def kind(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return "pdf"
    if ext in IMAGE_INPUT:
        return "image"
    raise ValueError(f"Unsupported file extension: {ext or '(none)'}")


def _image(path):
    with Image.open(path) as source:
        source.seek(0)
        image = ImageOps.exif_transpose(source)
        image.load()
        return image.copy()


def _save(image, target, fmt, quality=85):
    if fmt == "JPG":
        fmt = "JPEG"
    if fmt == "JPEG":
        if image.mode in ("RGBA", "LA", "P"):
            rgba = image.convert("RGBA")
            bg = Image.new("RGB", rgba.size, "white")
            bg.paste(rgba, mask=rgba.getchannel("A"))
            image = bg
        else:
            image = image.convert("RGB")
        image.save(target, format="JPEG", quality=quality, optimize=True)
    elif fmt == "WEBP":
        image.save(target, format="WEBP", quality=quality, method=4)
    elif fmt == "PDF":
        image.convert("RGB").save(target, format="PDF", resolution=150)
    elif fmt == "PNG":
        image.save(target, format="PNG", optimize=True)
    else:
        image.save(target, format=fmt)


def _atomic(target, work):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(f"Output exists: {target.name}")
    fd, tmp = tempfile.mkstemp(prefix=".jatayu-", suffix=target.suffix, dir=target.parent)
    os.close(fd)
    try:
        work(tmp)
        if not os.path.getsize(tmp):
            raise ValueError("Empty output")
        # Exclusive destination creation protects existing user data even on a race.
        os.link(tmp, target)
    finally:
        os.unlink(tmp)
    return str(target)


def _unique(folder, stem, ext):
    folder = Path(folder)
    for i in range(10000):
        name = stem + (f"-{i}" if i else "") + ext
        path = folder / name
        if not path.exists():
            return path
    raise ValueError("Too many files with this name")


def _run(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=900)
    if result.returncode:
        raise ValueError((result.stderr or result.stdout or "Processor failed").strip()[-500:])


def _render_pdf(path, dpi=150):
    with tempfile.TemporaryDirectory(prefix="jatayu-pdf-") as directory:
        prefix = str(Path(directory) / "page")
        _run(["pdftoppm", "-f", "1", "-r", str(dpi), "-png", str(path), prefix])
        pages = sorted(Path(directory).glob("page-*.png"),
                       key=lambda item: int(item.stem.rsplit('-', 1)[1]))
        if not pages:
            raise ValueError("No pages rendered; the PDF may be encrypted or damaged")
        for page in pages:
            yield _image(page)


def process_one(path, operation, output_dir, *, fmt="PNG", quality=85, width=0,
                height=0, keep_ratio=True, dpi=150, preset="Ebook", pages="all", rotation=90):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    source = kind(path)
    fmt = fmt.upper()
    quality = int(quality)
    if not 1 <= quality <= 100:
        raise ValueError("Quality must be 1–100")
    if operation in ("Convert", "PDF to images"):
        if source == "pdf":
            if fmt == "PDF":
                raise ValueError("Choose an image output for PDF conversion")
            outputs = []
            selected = set(parse_pages(pages, len(PdfReader(str(path)).pages)))
            for index, image in enumerate(_render_pdf(path, int(dpi)), 1):
                if index not in selected:
                    continue
                target = _unique(output_dir, f"{path.stem}-page-{index:03}", IMAGE_OUTPUT[fmt])
                outputs.append(_atomic(target, lambda tmp, im=image: _save(im, tmp, fmt, quality)))
            return outputs
        if operation == "PDF to images":
            raise ValueError("PDF to images requires a PDF input")
        target = _unique(output_dir, path.stem, IMAGE_OUTPUT[fmt])
        return [_atomic(target, lambda tmp: _save(_image(path), tmp, fmt, quality))]
    if operation == "Compress":
        if source == "pdf":
            if preset not in PDF_PRESETS:
                raise ValueError("Invalid PDF preset")
            target = _unique(output_dir, path.stem + "-compressed", ".pdf")
            def compress(tmp):
                _run(["gs", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite",
                      f"-dPDFSETTINGS={PDF_PRESETS[preset]}", f"-sOutputFile={tmp}", str(path)])
            return [_atomic(target, compress)]
        image = _image(path)
        out_fmt = "JPEG" if path.suffix.lower() in (".jpg", ".jpeg") else "WEBP" if path.suffix.lower() == ".webp" else "PNG"
        target = _unique(output_dir, path.stem + "-compressed", IMAGE_OUTPUT[out_fmt])
        return [_atomic(target, lambda tmp: _save(image, tmp, out_fmt, quality))]
    if operation == "Resize":
        if source != "image":
            raise ValueError("Resize supports images. Use Compress for PDF size reduction")
        width, height = int(width), int(height)
        if width < 0 or height < 0 or (width == 0 and height == 0):
            raise ValueError("Enter a positive width or height")
        image = _image(path)
        if keep_ratio:
            if width and height:
                image.thumbnail((width, height), Image.Resampling.LANCZOS)
            else:
                factor = (width / image.width) if width else (height / image.height)
                image = image.resize((max(1, round(image.width * factor)), max(1, round(image.height * factor))), Image.Resampling.LANCZOS)
        else:
            if not width or not height:
                raise ValueError("Enter both dimensions when aspect ratio is off")
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        if image.width * image.height > MAX_PIXELS:
            raise ValueError("Requested dimensions exceed the safety limit")
        out_fmt = fmt
        target = _unique(output_dir, path.stem + "-resized", IMAGE_OUTPUT[out_fmt])
        return [_atomic(target, lambda tmp: _save(image, tmp, out_fmt, quality))]
    if operation in ("Extract pages", "Split PDF", "Rotate PDF"):
        if source != "pdf":
            raise ValueError(f"{operation} requires a PDF input")
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            raise ValueError("Password-protected PDFs are not supported")
        selected = parse_pages(pages, len(reader.pages))
        if operation == "Split PDF":
            outputs = []
            for number in selected:
                target = _unique(output_dir, f"{path.stem}-page-{number:03}", ".pdf")
                def write_page(tmp, index=number):
                    writer = PdfWriter()
                    writer.add_page(reader.pages[index-1])
                    with open(tmp, "wb") as output:
                        writer.write(output)
                outputs.append(_atomic(target, write_page))
            return outputs
        target = _unique(output_dir, path.stem + ("-extracted" if operation == "Extract pages" else "-rotated"), ".pdf")
        def write_pdf(tmp):
            writer = PdfWriter()
            if operation == "Extract pages":
                for number in selected:
                    writer.add_page(reader.pages[number-1])
            else:
                degrees = int(rotation)
                if degrees not in (90, 180, 270):
                    raise ValueError("Rotation must be 90, 180 or 270 degrees")
                rotate_set = set(selected)
                for number, page in enumerate(reader.pages, 1):
                    added = writer.add_page(page)
                    if number in rotate_set:
                        added.rotate(degrees)
            with open(tmp, "wb") as output:
                writer.write(output)
        return [_atomic(target, write_pdf)]
    raise ValueError(f"Unknown operation: {operation}")


def parse_pages(spec, total):
    """Parse 1-based page selections, preserving explicit order and rejecting duplicates."""
    if total < 1:
        raise ValueError("PDF contains no pages")
    spec = str(spec or 'all').strip().lower().replace(' ', '')
    if spec in ('all', '*'):
        return list(range(1, total + 1))
    selected = []
    for token in spec.split(','):
        if '-' in token:
            fields = token.split('-')
            if len(fields) != 2 or not all(x.isdecimal() for x in fields):
                raise ValueError("Use page numbers such as 1-3,5")
            start, end = map(int, fields)
            if start > end:
                raise ValueError("Page ranges must ascend")
            selected.extend(range(start, end + 1))
        elif token.isdecimal():
            selected.append(int(token))
        else:
            raise ValueError("Use page numbers such as 1-3,5")
        if len(selected) > total:
            raise ValueError("Page selection repeats or exceeds the document")
    if not selected or len(selected) != len(set(selected)) or any(not 1 <= n <= total for n in selected):
        raise ValueError(f"Pages must be unique and between 1 and {total}")
    return selected


def merge(paths, output_dir, *, layout="PDF", columns=2, spacing=12, name="merged"):
    paths = [Path(p) for p in paths]
    if len(paths) < 2:
        raise ValueError("Select at least two files in the desired order")
    if layout == "PDF":
        target = _unique(output_dir, name, ".pdf")
        def write(tmp):
            writer = PdfWriter()
            for path in paths:
                if kind(path) == "pdf":
                    reader = PdfReader(str(path))
                    if reader.is_encrypted:
                        raise ValueError(f"Encrypted PDF is unsupported: {path.name}")
                    writer.append(reader)
                else:
                    im = _image(path).convert("RGB")
                    data = io.BytesIO()
                    im.save(data, format="PDF", resolution=150)
                    data.seek(0)
                    writer.append(PdfReader(data))
            with open(tmp, "wb") as output:
                writer.write(output)
        return _atomic(target, write)
    if any(kind(p) != "image" for p in paths):
        raise ValueError("Image layouts accept images only; choose PDF to mix PDFs and images")
    images = [_image(p).convert("RGBA") for p in paths]
    spacing = max(0, min(200, int(spacing)))
    if layout == "Vertical":
        cols = 1
    elif layout == "Horizontal":
        cols = len(images)
    elif layout == "Grid":
        cols = max(1, min(len(images), int(columns)))
    else:
        raise ValueError("Unknown merge layout")
    rows = math.ceil(len(images) / cols)
    cell_w = max(im.width for im in images)
    cell_h = max(im.height for im in images)
    out_w, out_h = cols * cell_w + (cols - 1) * spacing, rows * cell_h + (rows - 1) * spacing
    if out_w * out_h > MAX_PIXELS:
        raise ValueError("Merged image exceeds the safety limit")
    canvas = Image.new("RGBA", (out_w, out_h), "white")
    for i, im in enumerate(images):
        x, y = i % cols * (cell_w + spacing), i // cols * (cell_h + spacing)
        canvas.alpha_composite(im, (x, y))
    target = _unique(output_dir, name, ".png")
    return _atomic(target, lambda tmp: _save(canvas, tmp, "PNG"))
