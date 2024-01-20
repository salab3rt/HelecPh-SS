from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QMenu, QAction, QSystemTrayIcon, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pynput import mouse

class CaptureCoords:
    def __init__(self):
        self.initial_point = None
        self.final_point = None
        self.coords = {}

        self.app = QApplication([])
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set up system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self)
        menu = QMenu()
        get_coords_action = QAction('Get Coordinates', self)
        get_coords_action.triggered.connect(self.capture_coordinates)
        menu.addAction(get_coords_action)
        self.tray_icon.setContextMenu(menu)

    def on_click(self, x, y, button, pressed):
        if len(self.coords) < 2:
            if pressed and button == mouse.Button.left:
                self.initial_point = (x, y)
                self.draw_rectangle(x, y, x, y)  # Start drawing with initial point
            elif not pressed and button == mouse.Button.left:
                self.final_point = (x, y)
                key = f'bbox{len(self.coords) + 1}'
                self.coords[key] = self.initial_point + self.final_point
                self.initial_point = None
                self.final_point = None
        else:
            self.listener.stop()

    def on_move(self, x, y):
        if self.initial_point:
            self.draw_rectangle(self.initial_point[0], self.initial_point[1], x, y)

    def draw_rectangle(self, x1, y1, x2, y2):
        self.scene.clear()

        # Create a red rectangle item
        rect_item = QGraphicsRectItem(x1, y1, x2 - x1, y2 - y1)
        rect_item.setPen(Qt.red)
        self.scene.addItem(rect_item)

        self.view.show()

    def capture_coordinates(self):
        with mouse.Listener(on_click=self.on_click, on_move=self.on_move) as listener:
            self.listener = listener
            listener.join()
            self.view.hide()
            return self.coords

    def run(self):
        self.tray_icon.show()
        self.app.exec_()

# Example usage
if __name__ == "__main__":
    capture_coords = CaptureCoords()
    capture_coords.run()
