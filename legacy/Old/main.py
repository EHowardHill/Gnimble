from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QFontDatabase
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, QObject, Signal, Slot
import sys


class MainWindow(QObject):
    wordsCountChanged = Signal(str)

    def __init__(self):
        super().__init__()

        # Load the custom font
        font_id = QFontDatabase.addApplicationFont("Crimson_Text/CrimsonText-Regular.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font_bold_id = QFontDatabase.addApplicationFont("Crimson_Text/CrimsonText-Bold.ttf")
        font_bold_family = QFontDatabase.applicationFontFamilies(font_bold_id)[0]

        self.font_family = font_family
        self.font_bold_family = font_bold_family

    @Slot(str)
    def on_text_changed(self, text):
        count = len(text.split())
        self.wordsCountChanged.emit(f"Words: {count}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the view and load QML
    view = QQuickView()
    view.setSource(QUrl('main.qml'))

    # Set up the main window and expose it to QML
    main_window = MainWindow()
    context = view.rootContext()
    context.setContextProperty("mainWindow", main_window)

    view.show()

    sys.exit(app.exec_())
