import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: "Gnimble"

    // --------------------------------------------------
    // 1) Title Row
    // --------------------------------------------------

    Rectangle {
        id: rowContainer
        width: parent.width
        height: 24

        Row {
            id: rowTitle
            anchors.fill: parent // Make the Row fill the Rectangle
            spacing: 0

            Button {
                id: backButton
                text: "Back"
                width: 48
                height: 24

                // Set the text color to white
                contentItem: Text {
                    text: backButton.text
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    anchors.centerIn: parent
                }
            }

            TextEdit {
                id: labelTitle
                text: "My Document"
                anchors.verticalCenter: parent.verticalCenter
                horizontalAlignment: Text.AlignHCenter
                width: parent.width - backButton.width - saveButton.width
            }

            Button {
                id: saveButton
                text: "Save"
                width: 48
                height: 24

                // Set the text color to white
                contentItem: Text {
                    text: saveButton.text
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    anchors.centerIn: parent
                }
            }
        }
    }


    // --------------------------------------------------
    // 2) ToolBar
    // --------------------------------------------------
    ToolBar {
        id: toolbarMain
        anchors.top: rowContainer.bottom
        width: parent.width
        height: 40

        Row {
            anchors.left: parent.left

            // Define the colors

            // Reusable styled Button component
            Component {
                id: styledButton
                Button {
                    width: 40
                    height: 40
                    checkable: true  // Makes the button selectable

                    // Optional: Customize the text color for better contrast
                    contentItem: Text {
                        text: control.text
                        font.bold: control.font.bold
                        font.italic: control.font.italic
                        font.underline: control.font.underline
                        anchors.centerIn: parent
                    }
                }
            }

            Button {
                text: "B"
                font.bold: true
                width: 40
                height: 40
                onClicked: backend.buttonPushed() }
            Button { text: "I"
                font.italic: true
                width: 40
                height: 40 }
            Button { text: "U"
                font.underline: true
                width: 40
                height: 40 }
        }

        Row {
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter // Center the entire row vertically in the toolbar

            Rectangle {
                width: labelCount.implicitWidth + 20
                height: 32
                anchors.verticalCenter: parent.verticalCenter // Center each rectangle vertically in the row

                Label {
                    id: labelCount
                    anchors.centerIn: parent
                    text: "100 Words"
                }
            }

            Rectangle {
                width: labelBattery.implicitWidth + 20
                height: 32
                anchors.verticalCenter: parent.verticalCenter

                Label {
                    id: labelBattery
                    anchors.centerIn: parent
                    text: "80%"
                }
            }
        }

    }

    // --------------------------------------------------
    // 3) ScrollView (stacked below)
    // --------------------------------------------------
    ScrollView {
        id: view
        anchors.top: toolbarMain.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom

        TextArea {
            id: textArea
            objectName: "myTextArea"  // <--- give it an objectName for findChild
            textFormat: TextEdit.RichText
            wrapMode: TextEdit.Wrap
            leftPadding: 100
            rightPadding: 100
            topPadding: 20
            bottomPadding: 20
            placeholderText: qsTr("It was a dark and stormy night...")
        }
    }
}