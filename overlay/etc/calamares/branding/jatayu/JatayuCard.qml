// SPDX-License-Identifier: GPL-3.0-or-later
import QtQuick 2.5

Rectangle {
    id: card
    property string heading
    property string description
    property string tip
    property int number: 1
    color: "#10212d"
    radius: 12
    clip: true
    readonly property real scale: Math.min(width / 650, height / 430)

    Rectangle { width: parent.width / 3; height: 4; color: "#ff9933" }
    Rectangle { x: parent.width / 3; width: parent.width / 3; height: 4; color: "#f4f5f7" }
    Rectangle { x: parent.width * 2 / 3; width: parent.width / 3; height: 4; color: "#138808" }

    Image {
        x: 30 * card.scale; y: 22 * card.scale
        width: 64 * card.scale; height: width
        source: "logo.png"
        fillMode: Image.PreserveAspectFit
    }
    Text {
        x: 108 * card.scale; y: 30 * card.scale
        text: "JatayuOS 1.0 · Udaan"
        color: "#f5e3b0"; font.pixelSize: 21 * card.scale
        font.family: "Noto Sans"; font.bold: true
    }
    Text {
        x: 108 * card.scale; y: 59 * card.scale
        text: "Udaan Aapki. Shakti Bharat Ki."
        color: "#b9c9d5"; font.pixelSize: 13 * card.scale
    }
    Column {
        x: 32 * card.scale; y: 115 * card.scale
        width: parent.width - 64 * card.scale
        spacing: 18 * card.scale
        Text {
            width: parent.width; text: card.heading
            color: "#ffffff"; font.bold: true; font.family: "Noto Sans"
            font.pixelSize: 29 * card.scale; wrapMode: Text.WordWrap
        }
        Text {
            width: parent.width; text: card.description
            color: "#d4e0e8"; font.pixelSize: 18 * card.scale
            wrapMode: Text.WordWrap; lineHeight: 1.2
        }
        Rectangle {
            width: parent.width; height: note.implicitHeight + 24 * card.scale
            radius: 8; color: "#1d3545"
            Text {
                id: note
                x: 14 * card.scale; y: 12 * card.scale
                width: parent.width - 28 * card.scale
                text: card.tip; color: "#f0cf82"
                font.pixelSize: 14 * card.scale; wrapMode: Text.WordWrap
            }
        }
    }
    Row {
        anchors.bottom: parent.bottom; anchors.bottomMargin: 26 * card.scale
        anchors.left: parent.left; anchors.leftMargin: 32 * card.scale
        spacing: 8 * card.scale
        Repeater {
            model: 6
            Rectangle {
                width: 18 * card.scale; height: 5 * card.scale; radius: height / 2
                color: index + 1 === card.number ? "#efc76a" : "#48606f"
            }
        }
    }
    Text {
        anchors.right: parent.right; anchors.rightMargin: 30 * card.scale
        anchors.bottom: parent.bottom; anchors.bottomMargin: 22 * card.scale
        text: "Made in India  ·  jatayuos.in"
        color: "#b9c9d5"; font.pixelSize: 13 * card.scale
    }
}
