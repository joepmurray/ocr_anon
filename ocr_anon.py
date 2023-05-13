#-----------------------------------------------------------------------------------------------------------------
# ocr_anon.py
# Anonymizes an image file by searching for sensitive text, and redacting that text from the "burned-in" pixel data.
# Useful for removing protected healthcare information (PHI) from radiology/cardiology images so they can be used to
# train AI models without disclosing HIPAA-protected patient information.
#
# takes 2 arguments - a text string and a jpg file.  Uses easyocr optical character recognition to scan 
# the jpg file for the text string.  If it finds the text string in the image, it blocks it out by drawing a 
# solid box over the text pixel area, and creates a new output.jpg file
# Usage: python3 ocr_anon.py "PATIENT_NAME" ultrasound.jpg
#
# Future improvements: 
# - add multiple search strings (e.g. for name, and medical record number)
# - add the ability to fail or proceed based on low-probability matches from the OCR scan (need data to test)
# Joe Murray 5/13/2023
#--------------------------------------------------------------------------------------------------------------------

import cv2
import easyocr
import sys

def ocr_image(image_file, text_string):
  """
  Performs OCR on an image file and returns the text found.

  Args:
    image_file: The path to the image file.
    text_string: The text string to search for. 

  Returns:
    The text found in the image file.
  """

  # Load the image file.
  image = cv2.imread(image_file)

  # Convert the image to grayscale.
  grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Find the contours of the text in the image.
  contours, hierarchy = cv2.findContours(grayscale_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Extract the text from the image.
  reader = easyocr.Reader(["en"])
  text = reader.readtext(grayscale_image)
  # print(text)

  # Find the coordinates of the text found.
  coordinates = []
  for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    coordinates.append((x, y, w, h))

  # Return the text and coordinates found.
  return text, coordinates

def main():
  # Get the text string and image file name from the command line arguments.
  text_string = sys.argv[1]
  image_file = sys.argv[2]

  # Define the variable image.
  image = cv2.imread(image_file)

  # Perform OCR on the image file.
  text, coordinates = ocr_image(image_file, text_string)

  # print("main() text string",text_string)  
  # print("main() text variable",text)

  count=0
  for element in text:  
    if text_string in element:
      count += 1
      print(text_string, "is found in ", element)

      # Get the coordinates of the box.
      # print("coordinates of string are", element[0])
      text_coord = element[0]

      # Draw the box with blue border.
      # cv2.rectangle(image, (text_coord[0][0], text_coord[0][1]), (text_coord[2][0], text_coord[2][1]), (255, 0, 0), 2)

      # Draw the solid rectangle over the text. -1 fills the box
      cv2.rectangle(image, (text_coord[0][0], text_coord[0][1]), (text_coord[2][0], text_coord[2][1]), (255, 0, 0), -1)

      # create a new jpg output file
      cv2.imwrite("output.jpg", image)
        
  if (count == 0):
    print("The text string was not found in the image file.")
  else:
    print(count, " instances of ", text_string, " were found in the file ", image_file)

if __name__ == "__main__":
  main()
