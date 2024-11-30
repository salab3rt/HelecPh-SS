# HelecPh-SS

**HelecPh-SS** is a lightweight program that allows users to capture sections of their screen, perform OCR (Optical Character Recognition) on selected areas, and save the output with a user-defined (or OCR) filename in a specified folder. 

## Features

- **Screen Capture**: Capture specific sections of the screen by pressing `Ctrl + Space`.
- **OCR Integration**: Automatically recognize text from a selected section of the screen using Tesseract-OCR.
- **Custom Output**: Save captured screenshots and OCR results in a designated output folder.
- **System Tray**: Runs in the system tray for easy access to configuration options:
  - Select output folder.
  - Choose areas of the screen for OCR and capture.
  - Create profiles.

## Requirements

- **Tesseract-OCR**: Add a folder named `Tesseract-OCR` containing the necessary Tesseract-OCR files in the program's directory.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/salab3rt/HelecPh-SS.git
2. Install required dependencies (if applicable).
3. Add the `Tesseract-OCR` folder with all required Tesseract files in the program directory.
4. Run the program.

## Usage

1. Start the program. It will minimize to the system tray.
2. From the tray menu:
   - Set the output folder where files will be saved.
   - Select the sections of the screen for OCR and/or capture.
3. Press `Ctrl + Space` to start the screen capture process:
   - A prompt will appear for you to specify the filename.
   - The program will:
     - Capture the defined screen section.
     - Perform OCR on the selected area and recognize the text.
     - Save the screenshot with the recognized text as the filename.

## Shortcut

- **Ctrl + Space**: Start screen capture.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for the OCR functionality.
