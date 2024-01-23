import keyboard
from win32 import win32gui
import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QFileDialog, QInputDialog
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer
from screenshot import ScreenshotProcessor, CaptureCoords, resource_path
import threading
import time
import profiles

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

top_windows = []
win32gui.EnumWindows(windowEnumerationHandler, top_windows)
for i in top_windows:
    if "HemElec" in i[1]: #CHANGE PROGRAM TO THE NAME OF YOUR WINDOW
        sys.exit()

class ScreenshotApp(QWidget):
    def __init__(self):
        super().__init__()

        self.processor = ScreenshotProcessor()
        self.capture_coords = CaptureCoords(app)
        self.profiles_handler = profiles.UserCoordProfile()
        self.hotkey_pressed_time = 0
        try:
            self.current_profile = self.profiles_handler.current_profile
            self.capture_coords.coords = self.current_profile['coords']
            self.save_folder = self.current_profile['folder']
        except Exception as e:
            #print(e)
            self.save_folder = None
            self.capture_coords.coords = {}
        
        #print(self.capture_coords.coords)
        
        self.init_ui()
        
        app.setQuitOnLastWindowClosed(False)
        
        self.keyboard_timer = QTimer(self)
        self.keyboard_timer.timeout.connect(self.check_keyboard_input)
        self.keyboard_timer.start(100)
        #keyboard.add_hotkey("ctrl+space", self.on_hotkey_pressed, timeout=2)
        #keyboard.add_hotkey("ctrl+alt+e", self.close_app)

    def check_keyboard_input(self):
        if keyboard.is_pressed('ctrl+space'):
            self.on_hotkey_pressed()
        elif keyboard.is_pressed('ctrl+alt+e'):
            self.close_app()

    def init_ui(self):
        icon_path = resource_path("icon.png")
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        self.tray_icon.show()

        menu = QMenu()
        take_screenshot_action = QAction("Capturar Gráfico", self)
        take_screenshot_action.triggered.connect(self.take_screenshot_and_modify)
        menu.addAction(take_screenshot_action)
        
        self.profile_menu = menu.addMenu("Profiles")
        new_profile = QAction("Criar Perfil", self)
        new_profile.triggered.connect(self.create_and_save_profile)
        self.profile_menu.addAction(new_profile)
        
        for profile_name, _ in self.profiles_handler.profiles['profiles'].items():
            #print(profile_name)
            profile_action = QAction(profile_name, self)
            profile_action.triggered.connect(lambda _, profile_name=profile_name: self.switch_profile(profile_name))
            self.profile_menu.addAction(profile_action)

        get_coords_action = QAction("Definir Coordenadas", self)
        get_coords_action.triggered.connect(self.get_coords)
        menu.addAction(get_coords_action)
        
        save_directory_action = QAction('Selecionar Pasta', self)
        save_directory_action.triggered.connect(self.set_save_directory)
        menu.addAction(save_directory_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close_app)
        menu.addAction(exit_action)
        

        self.tray_icon.setContextMenu(menu)

    def on_hotkey_pressed(self):
        current_time = time.time()
        if current_time - self.hotkey_pressed_time > 0.5:
            # Create a new thread
            self.take_screenshot_and_modify()
            #threading.Thread(target=self.take_screenshot_and_modify).start()
            self.hotkey_pressed_time = current_time

    def take_screenshot_and_modify(self):
        if len(self.capture_coords.coords) == 2 and self.save_folder:
            image, text_region = self.processor.capture_screen_regions(self.capture_coords.coords)

            recognized_text = self.processor.recognize_text(text_region)
            
            text, ok_pressed = QInputDialog.getText(None, 'Amostra', 'Enter your text:', text=f'{recognized_text[:20] if recognized_text else "Não Reconhecido"}')
            if ok_pressed and text:
                self.tray_icon.showMessage("Amostra:", text, QSystemTrayIcon.MessageIcon.Information, 1000)
                #threading.Thread(target=self.take_screenshot_and_modify).start()
                threading.Thread(target=self.processor.save_cut_section, args=[image, text, self.save_folder]).start()
                #self.processor.save_cut_section(image, text, self.save_folder)

        else:
            self.tray_icon.showMessage("Configurações", 'Definir configurações', QSystemTrayIcon.MessageIcon.Warning, 2000)
            
    def create_and_save_profile(self, new_profile_name):
        if self.capture_coords.coords and self.save_folder:
            new_profile_name, ok = QInputDialog.getText(None, "New Profile", "Enter profile name:")
            
            if ok and new_profile_name and self.capture_coords.coords and self.save_folder:
                new_profile = {
                                'coords': self.capture_coords.coords.copy(),
                                'folder': self.save_folder
                            }
                #print(new_profile)
                try:
                    self.profiles_handler.save_profile(new_profile_name, new_profile)
                    profile_action = QAction(new_profile_name, self)
                    profile_action.triggered.connect(lambda _, profile_name=new_profile_name: self.switch_profile(profile_name))
                    self.profile_menu.addAction(profile_action)
                    self.profiles_handler.profiles = self.profiles_handler.load_profiles()
                except Exception as e:
                    print(e)
                    self.tray_icon.showMessage("Perfil", 'Falha ao adicionar perfil', QSystemTrayIcon.MessageIcon.Warning, 2000)
                    
        else:
            self.tray_icon.showMessage("Configurações", 'Definir configurações', QSystemTrayIcon.MessageIcon.Warning, 2000)
            
    def get_coords(self):
        
        self.capture_coords.show()
        #coords = self.capture_coords.capture_coordinates()
        #print(coords)
        
    def switch_profile(self, profile_name):
        self.profiles_handler.current_profile = self.profiles_handler.profiles['profiles'][profile_name]
        self.capture_coords.coords = self.profiles_handler.current_profile['coords']
        self.save_folder = self.profiles_handler.current_profile['folder']

    def set_save_directory(self):
        self.save_folder = None

        options = QFileDialog.Option.ShowDirsOnly
        #options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar Pasta", options=options)
        if directory:
            #print("Selected Directory:", directory)
            self.save_folder = directory


    def close_app(self):
        app.closeAllWindows()
        sys.exit(app.exit())

if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("HemElec")
    app.setStyle("Fusion")
    screenshot_app = ScreenshotApp()
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt and Exception as e:
        if e:
            print(f"Exception: {e}")
    finally:
        app.closeAllWindows()
        sys.exit(app.exit())
