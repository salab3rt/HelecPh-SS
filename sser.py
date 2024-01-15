import keyboard
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QCursor
from helpers.screenshot import ScreenshotProcessor, CaptureCoords
import threading
class ScreenshotApp(QWidget):
    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.processor = ScreenshotProcessor()
        self.capture_coords = CaptureCoords()
        self.init_ui()
        
        app.setQuitOnLastWindowClosed(False)
        keyboard.add_hotkey("ctrl+space", self.on_hotkey_pressed)
        keyboard.add_hotkey("ctrl+alt+e", self.close_app)

    def init_ui(self):
        self.tray_icon = QSystemTrayIcon(QIcon("helpers/icon.png"), self)
        self.tray_icon.show()

        menu = QMenu()

        take_screenshot_action = QAction("Take Screenshot and Modify", self)
        take_screenshot_action.triggered.connect(self.take_screenshot_and_modify)
        menu.addAction(take_screenshot_action)

        get_coords_action = QAction("Capture Coordinates", self)
        get_coords_action.triggered.connect(self.get_coords)
        menu.addAction(get_coords_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close_app)
        menu.addAction(exit_action)
        
        

        self.tray_icon.setContextMenu(menu)

    def on_hotkey_pressed(self):
        # Create a new thread when the hotkey is pressed
        threading.Thread(target=self.take_screenshot_and_modify).start()

    def take_screenshot_and_modify(self):
        if len(self.capture_coords.coords) == 2:
            image, text_region = self.processor.capture_screen_regions(self.capture_coords.coords)

            #image.show()
            recognized_text = self.processor.recognize_text(text_region)
            self.processor.save_cut_section(image, recognized_text)
            self.tray_icon.showMessage("Amostra:", recognized_text, QSystemTrayIcon.Information, 2000)
        else:
            self.tray_icon.showMessage("Coords", 'definir coordenadas', QSystemTrayIcon.Information, 2000)
            
        
    def get_coords(self):
        self.capture_coords.capture_coordinates()



    def close_app(self):
        self.tray_icon.hide()
        self.close()
        app.quit()


if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("Elec. Hem SS")
    screenshot_app = ScreenshotApp()
    try:
        app.exec_()
    except KeyboardInterrupt:
        app.quit()
    except Exception as e:
        print(f"Exception: {e}")
