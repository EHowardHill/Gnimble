import QtQuick 2.12
import QtQuick.Controls 2.12

ApplicationWindow {
    visible: true
    title: "Gnimble"
    width: 800
    height: 600

    background: Image {
        source: "beach.jpg"
        fillMode: Image.PreserveAspectCrop
    }

    menuBar: MenuBar {
        font.family: mainWindow.font_family
        background: Rectangle {
            color: "rgba(255, 255, 255, 0.75)"
        }

        Menu {
            title: "File"
            MenuItem { text: "New"; font.family: mainWindow.font_family }
            MenuItem { text: "Open..."; font.family: mainWindow.font_family }
            MenuItem { text: "Save"; font.family: mainWindow.font_family }
            MenuItem { text: "Exit"; font.family: mainWindow.font_family }
        }

        Menu {
            title: "Edit"
            MenuItem { text: "Undo"; font.family: mainWindow.font_family }
            MenuItem { text: "Redo"; font.family: mainWindow.font_family }
            MenuItem { text: "Cut"; font.family: mainWindow.font_family }
            MenuItem { text: "Copy"; font.family: mainWindow.font_family }
            MenuItem { text: "Paste"; font.family: mainWindow.font_family }
        }

        MenuItem {
            text: "Chapter One"
            font.family: mainWindow.font_bold_family
        }
    }

    TextArea {
        id: textArea
        anchors.fill: parent
        font.family: mainWindow.font_family
        font.pixelSize: 16
        color: "black"
        background: Rectangle {
            color: "rgba(255, 255, 255, 0.75)"
        }
        cursorVisible: true
        cursorWidth: 2
        cursorPosition: 0
        textFormat: TextEdit.PlainText
        onTextChanged: mainWindow.on_text_changed(text)
    }

    Rectangle {
        id: statusBar
        width: parent.width
        height: 30
        anchors.bottom: parent.bottom
        color: "rgba(255, 255, 255, 0.75)"
        Text {
            id: wordCountText
            anchors.centerIn: parent
            text: "Words: 0"
            font.family: "YourFontFamily"
        }

        // Assuming you have a function to update word count
        onTextChanged: {
            let wordCount = textArea.text.length === 0 ? 0 : textArea.text.split(/\s+/).length;
            wordCountText.text = "Words: " + wordCount;
        }
    }
}
