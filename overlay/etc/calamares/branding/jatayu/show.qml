// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.5
import calamares.slideshow 1.0

Presentation {
    id: presentation
    mouseNavigation: false
    arrowNavigation: false
    keyShortcutsEnabled: false
    loopSlides: true
    function onActivate() { currentSlide = 0; advanceTimer.restart(); }
    function onLeave() { advanceTimer.stop(); }
    Timer {
        id: advanceTimer
        interval: 14000
        repeat: true
        running: presentation.activatedInCalamares
        onTriggered: presentation.goToNextSlide()
    }
    Slide {
        x: 0; y: 0; width: parent.width; height: parent.height
        JatayuCard {
            anchors.fill: parent; number: 1
            heading: "Your next journey begins"
            description: "Welcome to JatayuOS: a desktop made in India, built on Debian and KDE Plasma. Udaan brings familiar tools and room to make the desktop your own."
            tip: "Installation is in progress. Keep your computer connected to power."
        }
    }
    Slide {
        x: 0; y: 0; width: parent.width; height: parent.height
        JatayuCard {
            anchors.fill: parent; number: 2
            heading: "A desktop that feels like yours"
            description: "Explore KDE Plasma with a familiar bottom panel, clear application menus and flexible settings. Manage your folders, drives and shortcuts with Dolphin."
            tip: "After installation, open System Settings to adjust display, input and appearance."
        }
    }
    Slide {
        x: 0; y: 0; width: parent.width; height: parent.height
        JatayuCard {
            anchors.fill: parent; number: 3
            heading: "Ready for everyday work"
            description: "Browse with Firefox ESR. Write documents, build spreadsheets and create presentations with LibreOffice. Kate, Okular and Ark cover editing, reading and archives."
            tip: "Your applications stay accessible from the menu and pinned panel shortcuts."
        }
    }
    Slide {
        x: 0; y: 0; width: parent.width; height: parent.height
        JatayuCard {
            anchors.fill: parent; number: 4
            heading: "Meet your Jatayu tools"
            description: "Start with Aarambh for useful shortcuts and offline help. Explore Jatayu Editing Tools, Wallpaper Changer and the Kavach, Sarkar Setu and Utsav web apps."
            tip: "Bhasa Setu helps with input setup. Waydroid needs a separate Android image and setup."
        }
    }
    Slide {
        x: 0; y: 0; width: parent.width; height: parent.height
        JatayuCard {
            anchors.fill: parent; number: 5
            heading: "Keep your system up to date"
            description: "Use the software tools to review available updates. Keep backups of important files and install software from trusted sources. Check permissions before adding apps."
            tip: "Open About JatayuOS for credits, legal information and update guidance."
        }
    }
    Slide {
        x: 0; y: 0; width: parent.width; height: parent.height
        JatayuCard {
            anchors.fill: parent; number: 6
            heading: "Help is already on your desktop"
            description: "The User Manual and FAQ are available offline. Visit jatayuos.in for the project website. After a successful installation, restart and remove the USB when prompted."
            tip: "Wait for the installer to finish before restarting. Your journey continues with Udaan."
        }
    }
}
