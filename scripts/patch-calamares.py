#!/usr/bin/env python3
"""Asserted Calamares 3.3.14 UI and partition-safety adjustments."""
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
    '''#include <QAbstractItemView>
#include <QProxyStyle>
#include <QApplication>

// QComboBox's menu-style popup ignores maxVisibleItems and grows to screen height.
// Use a scrolling list popup for the locale selector.
class JatayuLanguageStyle : public QProxyStyle
{
public:
    JatayuLanguageStyle() : QProxyStyle( QStringLiteral( "Fusion" ) ) {}
    int styleHint( StyleHint hint, const QStyleOption* option = nullptr,
                   const QWidget* widget = nullptr, QStyleHintReturn* data = nullptr ) const override
    {
        if ( hint == QStyle::SH_ComboBox_Popup ) return 0;
        return QProxyStyle::styleHint( hint, option, widget, data );
    }
};
''')
replace("src/modules/welcome/WelcomePage.cpp",
    '    ui->languageWidget->setModel( m_conf->languagesModel() );\n',
    '''    // Bound the locale popup on small VM and physical displays.
    auto* localeStyle = new JatayuLanguageStyle;
    localeStyle->setParent( ui->languageWidget );
    ui->languageWidget->setStyle( localeStyle );
    ui->languageWidget->setStyleSheet( QStringLiteral( "combobox-popup: 0;" ) );
    ui->languageWidget->setMaxVisibleItems( 8 );
    ui->languageWidget->setModel( m_conf->languagesModel() );
    ui->languageWidget->view()->setMaximumHeight( 280 );
''')
print("Calamares UI patch applied")

# Render each locale as one elided label rather than two distant text columns.
replace("src/modules/welcome/WelcomePage.cpp",
    '''    QStyledItemDelegate::paint( painter, option, index );
    option.widget->style()->drawItemText(
        painter,
        option.rect,
        Qt::AlignRight | Qt::AlignVCenter,
        option.palette,
        false,
        index.data( Calamares::Locale::TranslationsModel::EnglishLabelRole ).toString() );''',
    '''    QStyleOptionViewItem item( option );
    initStyleOption( &item, index );
    const QString english = index.data( Calamares::Locale::TranslationsModel::EnglishLabelRole ).toString();
    if ( !english.isEmpty() && english != item.text )
        item.text += QStringLiteral( " (%1)" ).arg( english );
    item.textElideMode = Qt::ElideRight;
    const QStyle* style = item.widget ? item.widget->style() : QApplication::style();
    style->drawControl( QStyle::CE_ItemViewItem, &item, painter, item.widget );''')

# Refuse destructive plans before any partition jobs run. Use the immutable
# on-disk model: the preview may already have changed the filesystem type.
replace("src/modules/partition/core/PartitionCoreModule.cpp",
    '#include <QDir>\n',
    '''#include <QDir>

// Keep Windows data and existing EFI partitions out of destructive plans.
class JatayuProtectedPartitionJob : public Calamares::Job
{
public:
    QString prettyName() const override { return QStringLiteral( "Preserve Windows and EFI partitions" ); }
    Calamares::JobResult exec() override
    {
        return Calamares::JobResult::error(
            QStringLiteral( "Windows / EFI partition protection" ),
            QStringLiteral( "This plan would erase an existing NTFS or EFI system partition. "
                            "Go back, install in free space, and reuse the EFI partition at "
                            "/boot/efi without formatting it. Erasing a disk containing these "
                            "partitions is disabled in this release." ) );
    }
};
''')
replace("src/modules/partition/core/PartitionCoreModule.cpp",
    '''    // The automountControl job goes in the list twice: the first
''',
    '''    // Check the entire plan before unmounting or making disk changes.
    for ( const auto* info : m_deviceInfos )
    {
        const auto* original = info->immutableDevice.data();
        if ( !original->partitionTable() ) continue;
        QStringList protectedPaths;
        for ( auto it = PartitionIterator::begin( original->partitionTable() );
              it != PartitionIterator::end( original->partitionTable() ); ++it )
        {
            const auto* partition = *it;
            if ( partition && ( partition->fileSystem().type() == FileSystem::Ntfs
                                || PartUtils::isEfiBootable( partition ) ) )
                protectedPaths << partition->partitionPath();
        }
        if ( protectedPaths.isEmpty() ) continue;
        for ( const auto& planned : info->jobs() )
        {
            const auto* table = dynamic_cast< CreatePartitionTableJob* >( planned.data() );
            const auto* format = dynamic_cast< FormatPartitionJob* >( planned.data() );
            const auto* remove = dynamic_cast< DeletePartitionJob* >( planned.data() );
            const auto* partition = format ? format->partition() : ( remove ? remove->partition() : nullptr );
            if ( table || ( partition && protectedPaths.contains( partition->partitionPath() ) ) )
                return Calamares::JobList { Calamares::job_ptr( new JatayuProtectedPartitionJob ) };
        }
    }

    // The automountControl job goes in the list twice: the first
''')
