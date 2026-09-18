import builtins
from platform import python_version
from sys import argv, exit, path
import PySide6.QtWidgets as pywidget
import PySide6 as pyside
import PySide6.QtGui as pygui
import PySide6.QtCore as pycore
import PySide6.QtWidgets as pyqt
from tkinter import filedialog
import io
import contextlib
from site import getsitepackages



app = pyqt.QApplication.instance()
if app is None:
    app = pywidget.QApplication(argv)


font_size: int = 16
version: float = 0.01
version_type: str = "Alpha"

window = pywidget.QWidget()
window.setWindowTitle("Pynotes")
layout = pywidget.QVBoxLayout()

font_label = pywidget.QLabel(f"Font Size {font_size}:")
layout.addWidget(font_label)

ide_info = pywidget.QLabel(f"Small-Code Version: {version, version_type} Python Version: {python_version()}")
ide_info.setWordWrap(True)
layout.addWidget(ide_info)

entry = pywidget.QTextEdit()
layout.addWidget(entry)

output_label = pywidget.QLabel("Debug output:")
output_label.setWordWrap(True)
layout.addWidget(output_label)

window.setLayout(layout)
window.show()

custom_font = pygui.QFont("Consolas", font_size)
entry.setFont(custom_font)


def save():
    file = filedialog.asksaveasfilename(title="Save File", filetypes=(("Python File", "*.py"), ("All Files", "*.*")))
    get_entry = entry.toPlainText()
    if file:
        with open(file, "w") as f:
            f.write(get_entry)


def openf():
    file = filedialog.askopenfilename()
    if file:
        with open(file, "r") as f:
            entry.clear()
            entry.setText(f.read())


def bigger():
    global font_size
    global custom_font
    font_size += 1
    custom_font = pygui.QFont("Consolas", font_size)
    entry.setFont(custom_font)
    font_label.setText(f"Font Size: {font_size}")


def smaller():
    global font_size
    global custom_font
    font_size -= 1
    custom_font = pygui.QFont("Consolas", font_size)
    entry.setFont(custom_font)
    font_label.setText(f"Font Size {font_size}:")


def run():
    source_code = entry.toPlainText()
    output_buffer = io.StringIO()
    try:
        user_paths = getsitepackages()
        for paths in user_paths:
            if paths not in path:
                path.append(paths)
    except Exception:
        pass


    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(source_code, {}, {})
        result = output_buffer.getvalue()
        output_label.setStyleSheet("color:white")
        if not result:
            result = "No output and/or no input"
    except Exception as e:
        result = f"Error: {e}"
        output_label.setStyleSheet("color: red")

    output_label.setText(f"Debug output: \n {result}")


runVar = pygui.QShortcut(pygui.QKeySequence("F5"), window)
runVar.activated.connect(run)
save_button = pygui.QShortcut(pygui.QKeySequence("Ctrl+S"), window)
save_button.activated.connect(save)
open_button = pygui.QShortcut(pygui.QKeySequence("Ctrl+O"), window)
open_button.activated.connect(openf)
bigger_font = pygui.QShortcut(pygui.QKeySequence("Ctrl+="), window)
bigger_font.activated.connect(bigger)
smaller_font = pygui.QShortcut(pygui.QKeySequence("Ctrl+-"), window)
smaller_font.activated.connect(smaller)

if __name__ == "__main__":
    exit(app.exec())
