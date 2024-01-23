from PIL import ImageGrab, ImageOps, Image, ImageFilter
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import QLabel, QWidget, QPushButton,QMessageBox
import pytesseract
import time, os, sys, re

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


tesseract_dir = resource_path('Tesseract-OCR')
    # Fallback for regular Python execution
pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_dir, "tesseract.exe")

class ScreenshotProcessor:
    def normalize_colors(self, image):

        grayscale_image = ImageOps.grayscale(image)
        inverted_image = ImageOps.invert(grayscale_image)
        #inverted_image.show()
        return inverted_image
        
    
            
    def capture_screen_regions(self, coords):
        def threshold_func(pixel_value):
            threshold = 127
            if pixel_value > threshold:
                return 0
            else:
                return 255
            
        screenshot = ImageGrab.grab()
        #print(coords)
        box1 = coords['bbox1']  # Replace with your actual coordinates
        box2 = coords['bbox2']  # Replace with your actual coordinates

        text_region = screenshot.crop(box1)
        text_region = text_region.resize((text_region.width * 3, text_region.height * 3), Image.BOX)
        text_region = text_region.filter(ImageFilter.SMOOTH_MORE)
        text_region = text_region.convert('L')
        text_region = text_region.point(threshold_func)
        text_region = ImageOps.invert(text_region)
        
        
        #text_region = self.normalize_colors(scaled_text_region)
        #text_region = self.normalize_colors(text_region)
        
        graph_region = screenshot.crop(box2)
        
        

        #text_region.show()
        
        return graph_region, text_region
    

    def recognize_text(self, image):
        # Use Tesseract OCR to recognize text from the image
        recognized_text = pytesseract.image_to_string(image, config='--psm 7')
        #print(recognized_text)
        
        char_mapping = {
                        '1': 'I',
                        '4': 'A',
                        '5': 'S',
                        '2': 'Z',
                        '0': 'O',
                        '8': 'B',
                        '*': 'X',
                        '¥': 'X',
                        'x': 'X'
                    }
        
        third_char_mapping = {
                                '0': 'O'
                            }
        modified_text = ''.join(char_mapping.get(char, char) for char in recognized_text[:2]) \
                        + ''.join(third_char_mapping.get(char, char) for char in recognized_text[2])\
                        + recognized_text[3:]
        
        pattern = re.compile(r'[^a-zA-Z0-9]+')
        cleaned_filename = re.sub(pattern, '', modified_text)
        
        
        return cleaned_filename
    
    def save_cut_section(self, image, filename, folder):
        try:
            
            filename = f"{filename if filename else str(time.time())}.jpg"
            target = folder + '/' + filename
            image.save(target)
        except Exception as e:
            print(e)

    
    
    
class CaptureCoords(QWidget):
    def __init__(self, app):
        super().__init__()

        self.setWindowTitle("Overlay")
        available_geometry = app.primaryScreen().availableGeometry()
        self.setGeometry(available_geometry)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        # Set semi-transparent background
        #self.opacity_effect = QGraphicsOpacityEffect(self)
        #self.opacity_effect.setOpacity(0.5)

        self.overlay_label = QWidget(self)
        self.overlay_label.setGeometry(0, 0, self.width(), self.height())
        self.overlay_label.setStyleSheet("background-color: rgba(0, 0, 0, 128);")
        #self.overlay_label.setGraphicsEffect(self.opacity_effect)

        self.initial_point = None
        self.final_point = None
        self.rect_coords = []
        self.coords = {}
        #print(self.coords)
        
        self.confirm_button = QPushButton("OK", self)
        self.confirm_button.setGeometry(10, 10, 50, 30)
        self.confirm_button.clicked.connect(self.showDialogOk)
        
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setGeometry(70, 10, 70, 30)
        self.cancel_button.clicked.connect(self.showDialogCancel)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.showDialogCancel()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            
            self.initial_point = event.pos()
            
        if event.button() == Qt.MouseButton.RightButton:

            if len(self.rect_coords) > 0:
                last_drawn_label = self.findChildren(QLabel)
                for label in last_drawn_label[1:]:
                    label.deleteLater()

                self.rect_coords.pop()
                
        self.show_drawn_rectangles()
        
        event.accept()  # Indicate that the event was handled

    def mouseMoveEvent(self, event):
        if event.button() != Qt.MouseButton.RightButton:
            # Update the final point on mouse move
            if self.initial_point:
                self.final_point = event.pos()
                # Draw the rectangle as the cursor moves
                self.draw_rectangle()
        

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Set the final point on mouse release
            self.final_point = event.pos()
            if self.initial_point != self.final_point:
                self.rect_coords.append([self.initial_point, self.final_point])
                self.draw_rectangle()
                self.show_drawn_rectangles()
                #print(self.rect_coords)
            self.initial_point = None
            self.final_point = None

    def draw_rectangle(self):
        # Clear any existing rectangles
        for label in self.findChildren(QLabel, name='current_rect')[1:]:
            label.deleteLater()
                
        if self.initial_point and self.final_point :
            rect = QRect(self.initial_point, self.final_point)
            # Draw the rectangle using a QLabel
            label = QLabel(self)
            label.setObjectName('current_rect')
            label.setGeometry(rect)
            label.setStyleSheet("border: 2px solid red; background-color: rgba(0, 0, 0, 0);")
            
            label.show()
            
    def show_drawn_rectangles(self):
        #print(self.rect_coords)
        if len(self.rect_coords) > 0:
            for rect in self.rect_coords:
                drawn_rect = QRect(rect[0], rect[1])
                drawn_rect_label = QLabel(self)
                drawn_rect_label.setObjectName('drawn_rects')
                drawn_rect_label.setGeometry(drawn_rect)
                drawn_rect_label.setStyleSheet("border: 2px solid red;")
                drawn_rect_label.show()
                
    def showDialogOk(self):
        reply = QMessageBox.question(self, "Confirmação", "Aceitar coordenadas?", QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:
            self.coords['bbox1'] = [self.rect_coords[0][0].x(), self.rect_coords[0][0].y(), self.rect_coords[0][1].x(), self.rect_coords[0][1].y()]
            self.coords['bbox2'] = [self.rect_coords[1][0].x(), self.rect_coords[1][0].y(), self.rect_coords[1][1].x(), self.rect_coords[1][1].y()]
            self.close()  # Close the overlay
            # Proceed with mor logic
    
    def showDialogCancel(self):
        self.initial_point = None
        self.final_point = None
        self.rect_coords = []
        self.close()
#class CaptureCoords:
#    def __init__(self):
#        self.initial_point = None
#        self.final_point = None
#        self.listener = None
#        self.coords = {}
#
#    def capture_coordinates(self):
#        #print("Click and drag to define a rectangle.")
#        self.coords = {}
#        try:
#            with mouse.Listener(on_click=self.on_click) as listener:
#                self.listener = listener
#                listener.join()
#        finally:
#            # Cleanup code
#            if self.listener:
#                self.listener.stop()
#            return self.coords
#
#    def on_click(self, x, y, button, pressed):
#        if len(self.coords) < 2:
#            if pressed and button == mouse.Button.left:
#                self.initial_point = (x, y)
#            elif not pressed and button == mouse.Button.left:
#                self.final_point = (x, y)
#                key = f'bbox{len(self.coords) + 1}'
#                self.coords[key] = self.initial_point + self.final_point
#                #print(self.coords)
#                self.initial_point = None
#                self.final_point = None
#        else:
#            self.listener.stop()
        






