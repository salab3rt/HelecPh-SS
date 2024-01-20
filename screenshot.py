from PIL import ImageGrab, ImageOps, ImageStat
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

    
    
    def normalize_colors(self, image):

        grayscale_image = ImageOps.grayscale(image)
        inverted_image = ImageOps.invert(grayscale_image)
        
        #inverted_image.show()
        return inverted_image
    

    def capture_screen_regions(self, coords):
        # Take a screenshot of the entire screen
        screenshot = ImageGrab.grab()
        #print(coords)
        box1 = coords['bbox1']  # Replace with your actual coordinates
        box2 = coords['bbox2']  # Replace with your actual coordinates

        text_region = screenshot.crop(box1)
        
        scaled_text_region = text_region.resize((text_region.width * 10, text_region.height * 10))
        
        text_region = self.normalize_colors(scaled_text_region)
        
        
        #stat = ImageStat.Stat(text_region)
        #mean_color = stat.mean[:3]
    
        #print(mean_color)
        #if mean_color[0] < 100:
        #    threshold = 150
        #    text_region = text_region.point(lambda i: i if i > threshold else 0)
        #else:
        #    threshold = 200
        #    text_region = text_region.point(lambda i: i if i < threshold else 255)
            
        #text_region.show()
        

        graph_region = screenshot.crop(box2)
        
        return graph_region, text_region
    

    def recognize_text(self, image):
        # Use Tesseract OCR to recognize text from the image
        recognized_text = pytesseract.image_to_string(image, config='--psm 8 -l eng')
        
        char_mapping = {
                        '1': 'I',
                        '4': 'A',
                        '5': 'S',
                        '2': 'Z',
                        '0': 'O',
                        '8': 'B'
                    }
        
        pattern = re.compile(r'[^a-zA-Z0-9]+')
        cleaned_filename = re.sub(pattern, '', recognized_text)
        
        modified_text = ''.join(char_mapping.get(char, char) for char in cleaned_filename[:2]) + cleaned_filename[2:]
        
        #print(modified_text)
        return modified_text
    
    def save_cut_section(self, image, filename, folder):
        try:
            
            filename = f"{filename if filename else str(time.time())}.jpg"
            target = folder + '/' + filename
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




