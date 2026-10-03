# JatayuOS installation slides

Six local QML slides introduce Udaan, KDE Plasma and Dolphin, everyday
applications, Jatayu tools, update habits, and offline documentation.
Each uses the official shield, tagline, Made in India, and jatayuos.in.
The presentation advances every 14 seconds, loops, and stops on exit.
It has no network dependency, video, or animated background.

The presentation and reusable card are in
`overlay/etc/calamares/branding/jatayu/`. Branding selects `show.qml` with
Calamares slideshow API 2. The integration package installs both QML files
and the existing official logo.

All six slides were rendered locally using Qt Quick's software backend and
Calamares 3.3.14's original Presentation/Slide QML components. Slide count,
wraparound, and exit lifecycle passed. The real installer presentation still
needs checking during the Windows dual-boot installation test.
