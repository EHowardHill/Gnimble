import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSlot

class Context(QObject):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine

    @pyqtSlot()
    def buttonPushed(self):
        """Toggle bold on the text selected in the QML TextArea."""
        root = self.engine.rootObjects()[0]
        textArea = root.findChild(QObject, "myTextArea")
        if not textArea:
            print("Couldn't find textArea")
            return

        # Retrieve properties we care about
        full_text = textArea.property("text")
        start = textArea.property("selectionStart")
        end = textArea.property("selectionEnd")

        if start == end:
            # If no selection, just flip the font.bold property
            # old_bold = textArea.property("font").get('bold')
            textArea.setProperty("font", {"bold": not False})
            return

        selected_text = full_text[start:end]
        # Very naive detection for <b>...</b>
        if selected_text.startswith("<b>") and selected_text.endswith("</b>"):
            selected_text = selected_text[3:-4]
        else:
            selected_text = f"<b>{selected_text}</b>"

        # Rebuild and set text
        prefix = full_text[:start]
        suffix = full_text[end:]
        new_text = prefix + selected_text + suffix
        textArea.setProperty("text", new_text)

        # Optionally reset selection
        textArea.setProperty("selectionStart", start)
        textArea.setProperty("selectionEnd", start + len(selected_text))

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
context = Context(engine)

engine.rootContext().setContextProperty("backend", context)
engine.load('main.qml')

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec_())
