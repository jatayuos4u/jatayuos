#!/usr/bin/env python3
"""Small, asserted Calamares 3.3.14 source adjustments for JatayuOS."""
from pathlib import Path

root = Path(__import__('sys').argv[1])
def replace(path, old, new):
    p = root / path
    data = p.read_text()
    if data.count(old) != 1:
        raise SystemExit(f"Unexpected Calamares source at {p}: expected one anchor, got {data.count(old)}")
    p.write_text(data.replace(old, new))

replace("src/modules/users/page_usersetup.ui",
    '    <widget class="QCheckBox" name="checkBoxRequireStrongPassword">',
    '''    <widget class="QCheckBox" name="showPasswords">
     <property name="text">
      <string>Show passwords</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QCheckBox" name="checkBoxRequireStrongPassword">''')
replace("src/modules/users/UsersPage.cpp",
    '    // Connect signals and slots\n',
    '''    // Reveal only while explicitly requested. Keep all password fields masked by default.
    connect( ui->showPasswords, &QCheckBox::toggled, this, [ this ]( bool shown )
    {
        const auto mode = shown ? QLineEdit::Normal : QLineEdit::Password;
        ui->textBoxUserPassword->setEchoMode( mode );
        ui->textBoxUserVerifiedPassword->setEchoMode( mode );
        ui->textBoxRootPassword->setEchoMode( mode );
        ui->textBoxVerifiedRootPassword->setEchoMode( mode );
    } );

    // Connect signals and slots
''')
replace("src/modules/welcome/WelcomePage.cpp",
    '#include <QApplication>\n',
    '#include <QAbstractItemView>\n#include <QApplication>\n')
replace("src/modules/welcome/WelcomePage.cpp",
    '    ui->languageWidget->setModel( m_conf->languagesModel() );\n',
    '''    // Bound the locale popup on small VM and physical displays.
    ui->languageWidget->setMaxVisibleItems( 8 );
    ui->languageWidget->view()->setMaximumHeight( 280 );
    ui->languageWidget->setModel( m_conf->languagesModel() );
''')
print("Calamares UI patch applied")
