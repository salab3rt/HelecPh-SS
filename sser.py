import keyboard
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget, QFileDialog
from PyQt5.QtGui import QIcon
from screenshot import ScreenshotProcessor, CaptureCoords, resource_path
import threading


class ScreenshotApp(QWidget):
    def __init__(self):
        super().__init__()

        self.processor = ScreenshotProcessor()
        self.capture_coords = CaptureCoords()
        self.save_folder = None
        self.init_ui()
        
        app.setQuitOnLastWindowClosed(False)
        keyboard.add_hotkey("ctrl+space", self.on_hotkey_pressed)
        keyboard.add_hotkey("ctrl+alt+e", self.close_app)

    def init_ui(self):
        icon_path = resource_path("icon.png")
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        self.tray_icon.show()

        menu = QMenu()

        take_screenshot_action = QAction("Capturar Gráfico", self)
        take_screenshot_action.triggered.connect(self.take_screenshot_and_modify)
        menu.addAction(take_screenshot_action)

        save_directory_action = QAction('Selecionar Pasta', self)
        save_directory_action.triggered.connect(self.set_save_directory)
        menu.addAction(save_directory_action)

        get_coords_action = QAction("Definir Coordenadas", self)
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
        if len(self.capture_coords.coords) == 2 and self.save_folder:
            image, text_region = self.processor.capture_screen_regions(self.capture_coords.coords)

            #image.show()
            recognized_text = self.processor.recognize_text(text_region)
            self.processor.save_cut_section(image, recognized_text, self.save_folder)
            if recognized_text:
                self.tray_icon.showMessage("Amostra:", recognized_text, QSystemTrayIcon.Information, 1500)
            else:
                self.tray_icon.showMessage("Amostra:", 'NÃO RECONHECIDO', QSystemTrayIcon.Information, 1500)
        else:
            self.tray_icon.showMessage("Coords", 'Definir configurações', QSystemTrayIcon.Warning, 2000)
            
        
    def get_coords(self):
        self.capture_coords.capture_coordinates()

    def set_save_directory(self):
        self.save_folder = None

        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar Pasta", options=options)
        if directory:
            #print("Selected Directory:", directory)
            self.save_folder = directory


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
