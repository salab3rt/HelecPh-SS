from PyQt5.QtWidgets import QApplication, QMenu, QAction, QMainWindow
from pynput import mouse
from pynput.mouse import Listener
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.capture_coords = CaptureCoords()

        self.init_ui()

    def init_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        get_coords_action = QAction('Get Coordinates', self)
        get_coords_action.triggered.connect(self.capture_coords.capture_coordinates)
        file_menu.addAction(get_coords_action)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Capture Coordinates Example')
        self.show()

class CaptureCoords:
    def __init__(self):
        self.initial_point = None
        self.final_point = None

    def capture_coordinates(self):
        print("Click and drag to define a rectangle.")
        with Listener(on_click=self.on_click) as listener:
            listener.join()

    def on_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            self.initial_point = (x, y)
        elif not pressed and button == mouse.Button.left:
            self.final_point = (x, y)
            print(f"Captured coordinates: {self.initial_point}, {self.final_point}")
            self.initial_point = None
            self.final_point = None

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    app.exec_()
