# ocr_anon.py
# Joe Murray 5/13/2023
# Python programs that anonymizes an image file by blocking out pixels containing text found (useful for anonymizing radiology scans by redacting Protected Healthcare Information 
# represented as 'burned-in pixel data, which is especially prevalent in Ultrasound scans and secondary capture radiology scans.  For research/AI development)
# anon_ocr.py:  uses easyocr library.  better for string searches, and grouping associated words
# anon_ocr_tesseract: uses the tesseract ocr library.  better for character searches.  program builds up strings from characters
