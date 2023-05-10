import pytesseract
import cv2


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

img = cv2.imread('./Images/new_image1.png')

# chuyển ảnh sang đen trắng
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# chuyển ảnh sang dạng nhị phân (binary)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# sử dụng pytesseract để nhận dạng chữ trong ảnh
text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')

print(text)
