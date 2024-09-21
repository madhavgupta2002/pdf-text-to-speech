import requests
import json
import base64
from gtts import gTTS
import os
from PyPDF2 import PdfReader, PdfWriter
import io
import re
from PIL import Image

def split_pdf(pdf_path):
    """
    Split a PDF file into individual pages.

    :param pdf_path: Path to the PDF file.
    :return: List of PDF pages as bytes objects.
    """
    pdf_pages = []
    pdf = PdfReader(pdf_path)
    for page in pdf.pages:
        writer = PdfWriter()
        writer.add_page(page)
        page_bytes = io.BytesIO()
        writer.write(page_bytes)
        pdf_pages.append(page_bytes.getvalue())
    return pdf_pages

def perform_ocr_on_pdf(pdf_path, api_key):
    """
    Perform OCR on a PDF file using OCR.space API.

    :param pdf_path: Path to the PDF file.
    :param api_key: OCR.space API key.
    :return: Extracted text from the PDF.
    """
    pdf_pages = split_pdf(pdf_path)
    extracted_text = ""

    for i, page_content in enumerate(pdf_pages):
        # Skip the page if it's larger than 1000 KB
        if len(page_content) > 1000 * 1024:
            print(f"Skipping page {i+1} due to large size")
            extracted_text += f" Page {i+1} skipped due to large size "
            continue

        # Encode the PDF content as base64
        pdf_base64 = base64.b64encode(page_content).decode('utf-8')

        # Set up the API request
        url = 'https://api.ocr.space/parse/image'
        payload = {
            'apikey': api_key,
            'base64Image': f'data:application/pdf;base64,{pdf_base64}',
            'language': 'eng',  # Change this if you need a different language
            'isOverlayRequired': False,
            'filetype': 'PDF',
            'detectOrientation': True,
            'scale': True,
            'OCREngine': 2,  # Use OCR Engine 2 for better results with PDFs
        }

        try:
            # Send the request to the API
            response = requests.post(url, data=payload)
            result = json.loads(response.content.decode())

            # Print the API response
            print(f"API Response for page {i+1}:")
            print(json.dumps(result, indent=2))

            # Check if the API request was successful
            if result['IsErroredOnProcessing']:
                raise Exception(f"OCR API Error on page {i+1}: {result['ErrorMessage']}")
            else:
                # Extract text from the page
                page_text = result['ParsedResults'][0]['ParsedText']
                extracted_text += page_text + " "

            print(f"Processed page {i+1}")

        except Exception as e:
            print(f"Error processing page {i+1}: {str(e)}")
            extracted_text += f" Page {i+1} skipped "

    # Remove unnecessary line breaks
    extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
    return extracted_text

def text_to_speech(text, output_audio_path, lang='en', slow=False):
    """
    Convert text to speech using the gTTS API and save it as an MP3 file.

    :param text: Text to convert to speech.
    :param output_audio_path: Path to save the output MP3 file.
    :param lang: The language for the speech (default is English).
    :param slow: Boolean indicating whether the speech should be slow.
    """
    try:
        # Initialize gTTS with the extracted text
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(output_audio_path)
        print(f"Audio has been saved to '{output_audio_path}'.")
    except Exception as e:
        print(f"An error occurred while converting text to speech: {e}")

def save_text_to_file(text, output_text_path):
    """
    Save the extracted text to a text file.

    :param text: Text to save.
    :param output_text_path: Path to save the output text file.
    """
    try:
        with open(output_text_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Extracted text has been saved to '{output_text_path}'.")
    except Exception as e:
        print(f"An error occurred while saving text to file: {e}")

def main():
    pdf_path = "sample.pdf"          # Replace with your PDF file path
    api_key = "K83149221088957"      # Replace with your OCR.space API key
    output_text_path = "output.txt"
    output_audio_path = "output.mp3"
    language = 'en'                  # Change language code if needed
    speech_speed = False             # Set to True for slower speech

    try:
        # Perform OCR on the PDF
        ocr_text = perform_ocr_on_pdf(pdf_path, api_key)
        print("OCR extraction successful.")

        # Save the extracted text to a file
        save_text_to_file(ocr_text, output_text_path)

        # Convert the extracted text to speech
        text_to_speech(ocr_text, output_audio_path, lang=language, slow=speech_speed)

        # Play the audio file
        try:
            if os.name == 'nt':
                os.startfile(output_audio_path)
            elif os.uname().sysname == 'Darwin':
                os.system(f"open {output_audio_path}")
            else:
                os.system(f"xdg-open {output_audio_path}")
            print("Playing the audio file...")
        except Exception as e:
            print(f"An error occurred while trying to play the audio: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
