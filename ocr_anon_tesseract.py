#-----------------------------------------------------------------------------------------------------------------
# ocr_anon_tesseract.py
# Joe Murray 5/13/2023
# Anonymizes an image file by searching for sensitive text, and redacting that text from the "burned-in" pixel data.
# Useful for removing protected healthcare information (PHI) from radiology/cardiology images so they can be used to
# train AI models without disclosing HIPAA-protected patient information.
#
# takes arguments - one or more text strings followed by a jpg file.  Uses tesseract optical character recognition to scan 
# the jpg file for the text string(s).  If it finds the text string in the image, it blocks it out by drawing a 
# solid box over the text pixel area, and creates a new output.jpg file
# tesseract doesn't do well with strings with a space, because it tokenizes words assembled by letters that are separated by spaces
#
# If you want to find "JOHN SMITH":
#    do this:  $ python ocr_anon_tesseract.py "JOHN" "SMITH" image.jpg
#    not this: $ python ocr_anon_tesseract.py "JOHN SMITH" image.jpg
#
# Future improvements: 
# - add multiple search strings (e.g. for name, medical record number, birthdate all in one OCR scan)
# - add the ability to fail or proceed based on low-probability matches from the OCR scan (need data to test)
# - any improvements to better integrate with DICOM file formats/transfer syntaxes directly for medical imaging workflows
# - deal with multibyte character sets, non-english, serif fonts, rotation, sideways text
#--------------------------------------------------------------------------------------------------------------------
import cv2
import sys
import os
import pytesseract
import pandas
import numpy as np

def main():
    # Get the text strings and image file name from the command line arguments.
    text_strings = sys.argv[1:-1]
    image_file = sys.argv[-1]

    # Set the Tesseract OCR command path based on the operating system
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' if os.name == 'nt' else '/usr/bin/tesseract'

    # Load the image file.
    image = cv2.imread(image_file)

    # Convert the image to grayscale.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # necessary for color images
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    df = pytesseract.image_to_data(threshold_img, lang="eng", config="--oem 3 --psm 6", output_type=pytesseract.Output.DATAFRAME)

    # Color
    red = (0, 0, 255)

    # print(df.keys())
    # print(df)

    count=0

    # For in all found texts
    for i in range(len(df['text'])):

      # If it finds the text string it will print the coordinates, and draw a rectangle around the word
      for text_string in text_strings:
        
        if text_string.lower() in str(df['text'][i]).lower():
          count += 1
          # print("found text!: ", text_string)
          # print(df['text'][i])
          # print(f"left: {df['left'][i]}")
          # print(f"top: {df['top'][i]}")
          # print(f"width: {df['width'][i]}")
          # print(f"height: {df['height'][i]}")

          # draw a solid rectangle over the found text
          cv2.rectangle(image, (df['left'][i], df['top'][i]), (df['left'][i]+df['width'][i], df['top'][i]+df['height'][i]), (255, 0, 0), -1)

          print("The text string:", text_string, "was found in the image file.")

    
    if (count > 0):
      # Split the filename into the name and extension
      f_name, f_extension = os.path.splitext(image_file)

      # Create the output file
      output_filename = f_name + "_anon" + f_extension

      # create a new jpg output file
      cv2.imwrite(output_filename, image)

if __name__ == "__main__":
    main()
