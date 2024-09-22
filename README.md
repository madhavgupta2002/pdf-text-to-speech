# PDF to Speech Converter

This Python script converts PDF files to speech by performing Optical Character Recognition (OCR) on the PDF and then converting the extracted text to audio.

## Features

- Split PDF files into individual pages
- Perform OCR on PDF files using the OCR.space API
- Convert extracted text to speech using Google Text-to-Speech (gTTS)
- Save extracted text to a file
- Play the generated audio file

## Requirements

- Python 3.6+
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - PyPDF2
  - gTTS
  - Pillow
  - tqdm

## Setup

1. Clone this repository:
   ```
   git clone github.com/madhavgupta2002/pdf-text-to-speech
   cd pdf-to-speech-converter
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Sign up for a free API key at [OCR.space](https://ocr.space/ocrapi)

4. Replace the `api_key` variable in the `main()` function with your OCR.space API key.

## Usage

1. Place your PDF file in the same directory as the script.

2. Update the `pdf_path` variable in the `main()` function with your PDF file name.

3. Run the script:
   ```
   python final_working.py
   ```

4. The script will perform OCR on the PDF, save the extracted text to `output.txt`, convert the text to speech, save it as `output.mp3`, and attempt to play the audio file.

## Customization

- Change the `language` variable in the `main()` function to convert text to speech in different languages (e.g., 'fr' for French, 'es' for Spanish).
- Set `speech_speed` to `True` in the `main()` function for slower speech output.

## Limitations

- The script may skip PDF pages larger than 1000 KB due to API limitations.
- The free OCR.space API has usage limits. For high-volume usage, consider upgrading to a paid plan.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](github.com/madhavgupta2002/pdf-text-to-speech/issues) if you want to contribute.

## Acknowledgements

- [OCR.space](https://ocr.space/) for providing the OCR API
- [Google Text-to-Speech (gTTS)](https://gtts.readthedocs.io/) for text-to-speech conversion
