from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QAction,
    QMainWindow,
    QHBoxLayout,
    QPlainTextEdit,
    QWidget,
    QMenuBar,
    QStatusBar
)
from PySide2.QtGui import QPalette, QColor, QFontDatabase, QFont
from PySide2.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Gnimble")

        self.setStyleSheet(
            """                                
            QMainWindow {
                border-image: url(beach.jpg) 0 0 0 0 scale;
            }
        """
        )

        # Load the custom font
        font_id = QFontDatabase.addApplicationFont("Crimson_Text/CrimsonText-Regular.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 12)
        self.setFont(font)

        font_bold_id = QFontDatabase.addApplicationFont("Crimson_Text/CrimsonText-Bold.ttf")
        font_bold_family = QFontDatabase.applicationFontFamilies(font_bold_id)[0]
        font_bold = QFont(font_bold_family, 12)

        # Create the menu bar
        menuBar = self.menuBar()
        menuBar.setFont(font)  # Apply the font to the menu bar

        chapterAction = QAction("Chapter One", self)
        chapterAction.setFont(font_bold)
        menuBar.addAction(chapterAction)
        menuBar.setStyleSheet("background-color: rgba(255, 255, 255, 0.75);")
        menuBar.addSeparator()

        # File menu
        fileMenu = menuBar.addMenu("File")

        # Add actions to File menu
        newAction = QAction("New", self)
        openAction = QAction("Open...", self)
        saveAction = QAction("Save", self)
        exitAction = QAction("Exit", self)

        # Set the font for each QAction
        newAction.setFont(font)
        openAction.setFont(font)
        saveAction.setFont(font)
        exitAction.setFont(font)

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        # Edit menu
        editMenu = menuBar.addMenu("Edit")

        # Add actions to Edit menu
        undoAction = QAction("Undo", self)
        redoAction = QAction("Redo", self)
        cutAction = QAction("Cut", self)
        copyAction = QAction("Copy", self)
        pasteAction = QAction("Paste", self)

        # Set the font for each QAction
        undoAction.setFont(font)
        redoAction.setFont(font)
        cutAction.setFont(font)
        copyAction.setFont(font)
        pasteAction.setFont(font)

        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        editMenu.addSeparator()
        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)

        # Set the background color to white
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.white))
        self.setPalette(palette)

        # Create a QPlainTextEdit and set its font
        self.text_edit = QPlainTextEdit()
        self.text_edit.setFont(font)  # Apply the custom font to QPlainTextEdit
        self.text_edit.setCursor(Qt.IBeamCursor)  # Set the type of cursor
        self.text_edit.setCursorWidth(2)
        QApplication.setCursorFlashTime(0)  # Disable cursor blinking
        self.text_edit.setStyleSheet(
            """                                
            QPlainTextEdit {
                color: black;
                background-color: rgba(255, 255, 255, 0.75);
            }
        """
        )
        self.text_edit.textChanged.connect(self.on_text_changed)

        # Create a central widget to hold the layout
        centralWidget = QWidget(self)
        mainVertical = QHBoxLayout(centralWidget)
        mainVertical.addWidget(self.text_edit)

        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("background-color: rgba(255, 255, 255, 0.75);")
        self.statusBar.showMessage("Words: 0")
        self.statusBar.setFont(font)
        self.setStatusBar(self.statusBar)

        # Set the central widget of the main window
        self.setCentralWidget(centralWidget)

    def on_text_changed(self):
        text = self.text_edit.toPlainText()
        count = len(text.split())
        self.statusBar.showMessage("Words: " + str(count))


# Create the application
app = QApplication(sys.argv)

# Create and show the main window
window = MainWindow()
window.show()

# Run the application
sys.exit(app.exec_())
