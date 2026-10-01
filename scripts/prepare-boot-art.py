#!/usr/bin/env python3
"""Build matching BIOS/UEFI boot art from the owner-supplied tricolor."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets' / 'india-tricolor.png'
LOGO = ROOT / 'assets' / 'logo.png'
OUT = ROOT / 'build' / 'config' / 'bootloaders'
if not SOURCE.is_file() or not LOGO.is_file():
    raise SystemExit('Missing owner-supplied tricolor or Jatayu logo')

def font(size):
    for name in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                 '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf'):
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()

def render(size, target):
    w, h = size
    with Image.open(SOURCE) as original:
        image = original.convert('RGB')
    ratio = max(w / image.width, h / image.height)
    image = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    x = (image.width - w) // 2
    y = (image.height - h) // 2
    image = image.crop((x, y, x + w, y + h)).convert('RGBA')
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    # The source remains visible; a translucent panel gives both loaders readable labels.
    draw.rounded_rectangle((int(.08*w), int(.38*h), int(.92*w), int(.82*h)),
                           radius=int(.024*w), fill=(6, 21, 32, 210), outline=(249, 196, 95, 240), width=max(2,w//320))
    draw.text((w//2, int(.065*h)), 'MADE IN INDIA', anchor='mt', font=font(round(.055*h)),
              fill=(10, 31, 48, 255), stroke_width=max(1,w//640), stroke_fill=(255, 255, 255, 220))
    image = Image.alpha_composite(image, layer)
    with Image.open(LOGO) as source_logo:
        mark = source_logo.convert('RGBA')
        mark.thumbnail((round(.15*h), round(.15*h)), Image.Resampling.LANCZOS)
    image.alpha_composite(mark, ((w-mark.width)//2, round(.17*h)))
    image = image.convert('RGB')
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, optimize=True)

render((640, 480), OUT/'syslinux_common'/'splash.png')
render((1920, 1080), OUT/'grub-pc'/'splash.png')
(OUT/'syslinux_common'/'stdmenu.cfg').write_text('''menu background splash.png
menu color title * #ffffffff #00000000 none
menu color border * #00000000 #00000000 none
menu color unsel * #ffffffff #00000000 none
menu color sel * #ffffffff #b02d814d none
menu color hotsel 1;7;37;40 #ffffffff #b02d814d none
menu color tabmsg * #ffffffff #00000000 none
menu color help * #ffffffff #00000000 none
menu width 60
menu hshift 12
menu margin 2
menu vshift 10
menu rows 5
menu helpmsgrow 16
menu cmdlinerow 17
menu timeoutrow 17
menu tabmsgrow 19
menu tabmsg Press ENTER to boot or TAB to edit an entry
''')
(OUT/'grub-pc'/'live-theme').mkdir(exist_ok=True)
(OUT/'grub-pc'/'live-theme'/'theme.txt').write_text('''desktop-image: "../splash.png"
title-text: ""
title-color: "#ffffff"
title-font: "Unifont Regular 16"
message-font: "Unifont Regular 16"
terminal-font: "Unifont Regular 16"
+ boot_menu {
    left = 15%
    width = 70%
    top = 45%
    height = 30%
    item_color = "#ffffff"
    item_font = "Unifont Regular 16"
    selected_item_color = "#ffd17b"
    selected_item_font = "Unifont Regular 16"
    item_height = 25
    item_spacing = 6
    item_padding = 5
}
+ progress_bar {
    id = "__timeout__"
    text = "Booting in %d s"
    left = 18%
    top = 78%
    width = 64%
    height = 12
    text_color = "#ffffff"
    fg_color = "#23804e"
    bg_color = "#163146"
    border_color = "#e6bd69"
}
''')
# Ensure firmware GRUB displays an actual countdown even if the stock template
# omitted a timeout; this config is shared by the ISO's BIOS/UEFI GRUB paths.
grub_cfg = OUT/'grub-pc'/'grub.cfg'
if not grub_cfg.is_file():
    raise SystemExit('Missing upstream GRUB template')
with grub_cfg.open('a') as config:
    config.write('\nset timeout_style=menu\nset timeout=8\n')
print('Rendered 640x480 BIOS and 1920x1080 UEFI tricolor menus.')

# Ship the same artwork and theme inside the installed root filesystem.
# ISO bootloader templates alone are not copied into the installed GRUB theme.
installed = ROOT/'build'/'config'/'includes.chroot'/'usr'/'share'/'grub'/'themes'/'jatayu'
installed.mkdir(parents=True, exist_ok=True)
render((1920, 1080), installed/'background.png')
theme = (OUT/'grub-pc'/'live-theme'/'theme.txt').read_text()
(installed/'theme.txt').write_text(theme.replace('../splash.png', 'background.png'))
print('Prepared persistent installed-system GRUB theme.')
