import pyautogui
from PIL import Image, ImageDraw
import io
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def take_screenshot_and_modify():
    # Take screenshot
    screenshot = pyautogui.screenshot()

    # Perform modifications using Pillow
    modified_image, cut_section = modify_image(screenshot)

    # Display the modified image (you can replace this with your logic)
    modified_image.show()

    # Use Tesseract OCR to recognize text from the cut section
    recognized_text = recognize_text(cut_section)

    # Save the cut section with a filename based on the recognized text
    save_cut_section(cut_section, recognized_text)
    

def modify_image(image):
    # Convert the screenshot to a Pillow Image object
    pil_image = Image.frombytes("RGB", image.size, image.tobytes())

    # Example modification: Draw a red rectangle on the image
    draw = ImageDraw.Draw(pil_image)
    draw.rectangle([120, 175, 250, 200], outline="red", width=2)

    # Cut the section based on specified coordinates
    cut_section = pil_image.crop((120, 175, 250, 200))

    return pil_image, cut_section

def get_serialized_icon():
    icon_image = Image.open("./helpers/icon.png")  # Replace with the actual path to your icon
    
    image_io = io.BytesIO()
    icon_image.save(image_io, format='PNG')
    return image_io.getvalue()


serialized_icon = get_serialized_icon()

def recognize_text(image):
    # Use Tesseract OCR to recognize text from the image
    recognized_text = pytesseract.image_to_string(image)
    return recognized_text

def save_cut_section(image, filename):
    try:
        filename = str(filename).replace('\n\n', '')
        print('FILENAME:',filename)
        # Save the cut section with a filename based on the recognized text
        image.save(f"{filename}.png")
    except Exception as e:
        print(e)
