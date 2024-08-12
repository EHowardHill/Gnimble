from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QAction,
    QMainWindow,
    QHBoxLayout,
    QPlainTextEdit,
    QWidget,
    QMenuBar,
    QStatusBar,
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QSizePolicy,
)
from PySide2.QtGui import QPalette, QColor, QFontDatabase, QFont
from PySide2.QtCore import Qt
import sys


class MenuBar(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.75);")

class ChapterButton(QHBoxLayout):
    text = ""

    def __init__(self, parent, text):
        super().__init__()

        self.text = text
        button_open = QPushButton(self.text)

        # Set size policy for button_open to expand horizontally
        button_open.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button_open.clicked.connect(lambda: parent.loadStory(self.text))

        self.addWidget(button_open)


class ChapterSelect(QWidget):

    def loadStory(self, text):
        print(text)
        self.parent.loadStory()

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # Load the custom font
        font_id = QFontDatabase.addApplicationFont(
            "Crimson_Text/CrimsonText-Regular.ttf"
        )
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 12)
        self.setFont(font)

        # Access the menuBar from the parent (MainWindow)
        self.menuBar = self.parent.menuBar

        # Clear existing actions (optional, if you want to replace the menu)
        self.menuBar.clear()

        # Add new actions or menus
        exitStory = self.menuBar.addMenu("Return")
        newChapter = self.menuBar.addMenu("New Chapter")

        # Create a QScrollArea
        mainLayout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a widget that will be inside the scroll area
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Add your buttons or other widgets to the scroll layout
        for i in range(10):  # Add multiple buttons for demonstration
            button = ChapterButton(self, "Chapter " + str(i))
            scroll_layout.addLayout(button)

        # Set the scroll content widget to the scroll area
        scroll_area.setWidget(scroll_content)

        # Add the scroll area to the main layout
        mainLayout.addWidget(scroll_area)

        self.parent.statusBar.showMessage("My Story: Story")


class DocumentEdit(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # Load the custom font
        font_id = QFontDatabase.addApplicationFont(
            "Crimson_Text/CrimsonText-Regular.ttf"
        )
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 12)
        self.setFont(font)

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

        # Create a layout to hold the text edit
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.text_edit)

        # Access the menuBar from the parent (MainWindow)
        self.menuBar = self.parent.menuBar

        # Clear existing actions (optional, if you want to replace the menu)
        self.menuBar.clear()

        # Add new actions or menus
        menuChapter = self.menuBar.addMenu("Chapter One")
        menuChapter.triggered.connect(lambda: parent.chapterSelect())
        self.menuBar.addMenu(menuChapter)

        # Set the layout to the central widget
        self.setLayout(mainLayout)

    def on_text_changed(self):
        text = self.text_edit.toPlainText()
        count = len(text.split())
        self.parent.statusBar.showMessage("Words: " + str(count))


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
        font_id = QFontDatabase.addApplicationFont(
            "Crimson_Text/CrimsonText-Regular.ttf"
        )
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 12)
        self.setFont(font)

        font_bold_id = QFontDatabase.addApplicationFont(
            "Crimson_Text/CrimsonText-Bold.ttf"
        )
        font_bold_family = QFontDatabase.applicationFontFamilies(font_bold_id)[0]
        font_bold = QFont(font_bold_family, 12)

        # Create the menu bar
        self.menuBar = self.menuBar()  # Use the built-in menu bar
        self.menuBar.setFont(font)  # Apply the font to the menu bar
        self.menuBar.setStyleSheet("background-color: rgba(255, 255, 255, 0.75);")

        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("background-color: rgba(255, 255, 255, 0.75);")
        self.statusBar.setFont(font)
        self.setStatusBar(self.statusBar)

        # Set the background color to white
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.white))
        self.setPalette(palette)

        self.mainPanel = ChapterSelect(self)

        # Set the central widget of the main window
        self.setCentralWidget(self.mainPanel)

    def loadStory(self):
        self.mainPanel.deleteLater()
        self.mainPanel = DocumentEdit(self)
        self.setCentralWidget(self.mainPanel)

    def chapterSelect(self):
        print("UH")
        self.mainPanel.deleteLater()
        self.mainPanel = ChapterSelect(self)
        self.setCentralWidget(self.mainPanel)

# Create the application
app = QApplication(sys.argv)

# Create and show the main window
window = MainWindow()
window.setFixedSize(320, 480)
window.show()

# Run the application
sys.exit(app.exec_())
