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
        color: "black" // Set the background color to black

        Row {
            id: rowTitle
            anchors.fill: parent // Make the Row fill the Rectangle
            spacing: 0

            Button {
                id: backButton
                text: "Back"
                width: 48
                height: 24

                // Customize the Button's appearance
                background: Rectangle {
                    color: "black" // Button background
                }

                // Set the text color to white
                contentItem: Text {
                    text: backButton.text
                    color: "white"
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    anchors.centerIn: parent
                }
            }

            Label {
                id: labelTitle
                text: "My Document"
                color: "white" // Set text color to white
                anchors.verticalCenter: parent.verticalCenter
                horizontalAlignment: Text.AlignHCenter
                width: parent.width - backButton.width - saveButton.width
            }

            Button {
                id: saveButton
                text: "Save"
                width: 48
                height: 24

                // Customize the Button's appearance
                background: Rectangle {
                    color: "black" // Button background
                }

                // Set the text color to white
                contentItem: Text {
                    text: saveButton.text
                    color: "white"
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

        // Define a custom background using a Rectangle
    background: Rectangle {
        anchors.fill: parent
        color: white
    }

    Row {
        anchors.left: parent.left

        Button {
            text: "B"
            font.bold: true
            width: 40
            height: 40 }
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
        spacing: 10
        anchors.verticalCenter: parent.verticalCenter // Center the entire row vertically in the toolbar

        Rectangle {
            width: labelCount.implicitWidth + 20
            height: 32
            radius: 4
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
            radius: 4
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
    wrapMode: TextEdit.Wrap
    leftPadding: 100
    rightPadding: 100
    topPadding: 20
    bottomPadding: 20
    placeholderText: qsTr("It was a dark and stormy night...")

    // Set the text color to white
    color: "white"

    // Define the background as a black rectangle
    background: Rectangle {
        color: "black"
        radius: 5 // Optional: Adds rounded corners
        // You can add borders or other styling here if desired
    }

    // Optional: Style the placeholder text
    placeholderTextColor: "lightgray"
}
    }
}