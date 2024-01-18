from PIL import ImageGrab, ImageEnhance
import pytesseract
import re
from pynput import mouse
import time
import os
import sys

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
    def capture_screen_regions(self, coords):
        # Take a screenshot of the entire screen
        screenshot = ImageGrab.grab()
        #print(coords)
        box1 = coords['bbox1']  # Replace with your actual coordinates
        box2 = coords['bbox2']  # Replace with your actual coordinates

        text_region = screenshot.crop(box1)
        scaled_text_region = text_region.resize((text_region.width * 4, text_region.height * 4))
        enhancer = ImageEnhance.Contrast(scaled_text_region)
        enhanced_text_region = enhancer.enhance(2.0)
        #enhanced_text_region.show()

        graph_region = screenshot.crop(box2)
        
        return graph_region, enhanced_text_region
    

    def recognize_text(self, image):
        # Use Tesseract OCR to recognize text from the image
        recognized_text = pytesseract.image_to_string(image)
        return recognized_text
    
    def save_cut_section(self, image, filename, folder):
        try:
            #print(folder)
            pattern = re.compile(r'[^\w]+')
            cleaned_filename = re.sub(pattern, '', filename)
            filename = f"{cleaned_filename if cleaned_filename else str(time.time())}.jpg"
            target = folder + '/' + filename
            #print(target)
            #print(cleaned_filename)
            #print('FILENAME:',filename)
            image.save(target)
        except Exception as e:
            print(e)

class CaptureCoords:
    def __init__(self):
        self.initial_point = None
        self.final_point = None
        self.listener = None
        self.coords = {}

    def capture_coordinates(self):
        #print("Click and drag to define a rectangle.")
        self.coords = {}
        try:
            with mouse.Listener(on_click=self.on_click) as listener:
                self.listener = listener
                listener.join()
        finally:
            # Cleanup code
            if self.listener:
                self.listener.stop()
            return self.coords

    def on_click(self, x, y, button, pressed):
        if len(self.coords) < 2:
            if pressed and button == mouse.Button.left:
                self.initial_point = (x, y)
            elif not pressed and button == mouse.Button.left:
                self.final_point = (x, y)
                key = f'bbox{len(self.coords) + 1}'
                self.coords[key] = self.initial_point + self.final_point
                #print(self.coords)
                self.initial_point = None
                self.final_point = None
        else:
            self.listener.stop()
        

#def get_serialized_icon():
#    icon_image = Image.open("./helpers/icon.png")  # Replace with the actual path to your icon
#    
#    image_io = io.BytesIO()
#    icon_image.save(image_io, format='PNG')
#    return image_io.getvalue()


#serialized_icon = get_serialized_icon()




