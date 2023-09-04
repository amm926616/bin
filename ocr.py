import pytesseract
from PIL import Image

# Open the image
image = Image.open('test.png')

# Use pytesseract to extract text
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)

