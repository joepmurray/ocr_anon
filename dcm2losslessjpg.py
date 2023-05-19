# dcm2losslessjpg.py
# 5/19/2023 Joe Murray
# opens a dicom file, prints any PHI data (pt name, mrn, dob), then saves the pixel data as lossless jpg.
# use as a pre-processor for dicom header and pixel data anonymization

import pydicom
import sys
import os
from PIL import Image

def main():
  # Get the DICOM file name from the command line.
  dicom_file_name = sys.argv[1]

  # Check to make sure that the DICOM file exists.
  if not os.path.exists(dicom_file_name):
    print(f"The DICOM file {dicom_file_name} does not exist.")
    sys.exit(1)

  # Read the DICOM file.
  try:
    dicom_file = pydicom.read_file(dicom_file_name)
  except FileNotFoundError as e:
    print(f"The DICOM file {dicom_file_name} could not be found.")
    sys.exit(1)

  # Get the PHI values: patient name, ID, and birth.

  # Check to see if the DICOM file has a PatientName tag.
  # if dicom_file.has_tag("PatientName"):
  if "PatientName" in dicom_file:
    # The DICOM file has a PatientName tag.
    patient_name = dicom_file.PatientName
  else:
    # The DICOM file does not have a PatientID tag.
    patient_name = None

  # Check to see if the DICOM file has a PatientID tag.
  # if dicom_file.has_tag("PatientID"):
  if "PatientID" in dicom_file:
    # The DICOM file has a PatientID tag.
    patient_id = dicom_file.PatientID
  else:
    # The DICOM file does not have a PatientID tag.
    patient_id = None

  # Check to see if the DICOM file has a PatientBirthDate tag.
  # if dicom_file.has_tag("PatientBirthDate"):
  if "PatientBirthDate" in dicom_file:
    # The DICOM file has a PatientBirthDate tag.
    patient_birth_date = dicom_file.PatientBirthDate
  else:
    # The DICOM file does not have a PatientID tag.
    patient_birth_date = None


  # Check to make sure that the patient name, ID, and birth date values are actually present in the DICOM file.
  if not patient_name:
    print("The patient name is not present in the DICOM file.")
  if not patient_id:
    print("The patient ID is not present in the DICOM file.")
  if not patient_birth_date:
    print("The patient birth date is not present in the DICOM file.")

  # Print out the patient name, ID, and birth date values.
  print(f"Patient name: {patient_name}")
  print(f"Patient ID: {patient_id}")
  print(f"Patient birth date: {patient_birth_date}")

  # Get the pixel data from the DICOM file.
  pixel_data = dicom_file.pixel_array

  # Convert the pixel data to a lossless JPEG image.
  image = Image.fromarray(pixel_data)


  # Split the filename into the name and extension
  f_name, f_extension = os.path.splitext(dicom_file_name)

  # Create the output file
  output_filename = f_name + ".jpg" 
 
  # Save the DICOM file as lossless JPG
  try:
    image.save(output_filename, "JPEG", quality=100)
    print(f"Wrote jpg file: {output_filename}")
  except FileNotFoundError as e:
    print(f"The output file {output_file_name} could not be created.")
    sys.exit(1)

if __name__ == "__main__":
  main()
