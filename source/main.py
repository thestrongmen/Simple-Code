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

app = pyqt.QApplication.instance() #instances QApplication
if app is None: # if there is no QApplication
    app = pywidget.QApplication(argv) #make a QApplication

#misc variables
font_size: int = 16
version: float = 0.01
version_type: str = "Alpha"

#window and layout
window = pywidget.QWidget()
window.setWindowTitle("Simple-Code")
layout = pywidget.QVBoxLayout()

#widgets
font_label = pywidget.QLabel(f"Font Size {font_size}:")
layout.addWidget(font_label)

ide_info = pywidget.QLabel(f"Simple-Code Version: {version, version_type} Python Version: {python_version()}")
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
    file = filedialog.asksaveasfilename(title="Save File", filetypes=(("Python File", "*.py"), ("All Files", "*.*"))) #asks to save file in either python files or all file types
    get_entry = entry.toPlainText() #get the text from the text box
    if file: #if a file is selected
        with open(file, "w") as f: #save and overwrite
            f.write(get_entry)#save an overwrite with the text from the text box


def openf():
    file = filedialog.askopenfilename() #asks to open file using tkinter's askopenfilename function
    if file: #if a file is selected
        with open(file, "r") as f: #read file
            entry.clear() #clear the text box
            entry.setText(f.read()) #sets the text box text to the opened file


def bigger():
    global font_size #gets the font size variable
    global custom_font #gets the custom font
    font_size += 1 #increases the font size
    custom_font = pygui.QFont("Consolas", font_size) #sets the custom font with the just increased font size
    entry.setFont(custom_font) #sets the text box to the custom font
    font_label.setText(f"Font Size {font_size}:") #label to see the font size


def smaller():
    global font_size #gets the font size variable
    global custom_font #gets the custom font
    font_size -= 1 #decreases the font size
    custom_font = pygui.QFont("Consolas", font_size) #sets the custom font with the just decreased font size
    entry.setFont(custom_font) #sets the text box to the custom font
    font_label.setText(f"Font Size {font_size}:") #label to see the font size

#debug console
def run():
    source_code = entry.toPlainText() #gets the code
    output_buffer = io.StringIO() #make a buffer
    try:
        user_paths = getsitepackages() #checks for packages
        for paths in user_paths: #a for loop "for paths in found packages"
            if paths not in path: #if a path is not in the sys.path then add it
                path.append(paths)
    except Exception:
        pass #if there are no packages or they were unable to load it passes

    try:
        with contextlib.redirect_stdout(output_buffer): #sends text to buffer
            exec(source_code, {}, {}) #the part that executes the code
        result = output_buffer.getvalue() #gets the value stored in the buffer
        output_label.setStyleSheet("color:white") #color is white indicating that it succeeded
        if not result:
            result = "No output and/or no input" #if there was no input and/or output it writes "No output and/or no input"
    except Exception as error: # if there was a error
        result = f"Error: {error}" # write the error
        output_label.setStyleSheet("color: red") #red to indicate that debugging was unsuccessful

    output_label.setText(f"Debug output: \n {result}") #print the result variable


run_var = pygui.QShortcut(pygui.QKeySequence("F5"), window) #debugging hotkey
run_var.activated.connect(run)
save_button = pygui.QShortcut(pygui.QKeySequence("Ctrl+S"), window) #saving hotkey
save_button.activated.connect(save)
open_button = pygui.QShortcut(pygui.QKeySequence("Ctrl+O"), window) #opening hotkey
open_button.activated.connect(openf)
bigger_font = pygui.QShortcut(pygui.QKeySequence("Ctrl+="), window) #zooming in hotkey
bigger_font.activated.connect(bigger)
smaller_font = pygui.QShortcut(pygui.QKeySequence("Ctrl+-"), window) #zooming out hotkey
smaller_font.activated.connect(smaller)

if __name__ == "__main__":
    exit(app.exec())
