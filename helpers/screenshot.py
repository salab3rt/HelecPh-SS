from PIL import Image, ImageDraw
import pyautogui
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScreenshotProcessor:
    def take_screenshot(self):
        return pyautogui.screenshot()

    def modify_image(self, image):
        # Convert the screenshot to a Pillow Image object
        pil_image = Image.frombytes("RGB", image.size, image.tobytes())

        draw = ImageDraw.Draw(pil_image)
        draw.rectangle([120, 175, 250, 200], outline="red", width=2)

        # Cut the section based on specified coordinates
        cut_section = pil_image.crop((120, 175, 250, 200))

        return pil_image, cut_section
    
    def recognize_text(self, image):
        # Use Tesseract OCR to recognize text from the image
        recognized_text = pytesseract.image_to_string(image)
        return recognized_text
    
    def save_cut_section(self, image, filename):
        try:
            filename = str(filename).replace('\n\n', '')
            print('FILENAME:',filename)
            image.save(f"{filename}.png")
        except Exception as e:
            print(e)

#def get_serialized_icon():
#    icon_image = Image.open("./helpers/icon.png")  # Replace with the actual path to your icon
#    
#    image_io = io.BytesIO()
#    icon_image.save(image_io, format='PNG')
#    return image_io.getvalue()


#serialized_icon = get_serialized_icon()




