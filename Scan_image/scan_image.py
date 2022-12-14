import pytesseract
import cv2
import numpy as np



def scan_image(name_image, language='eng'):
    image = cv2.imread('tests/' + name_image)

    print(pytesseract.image_to_string(image, lang=language))

scan_image('rus_photo1.jpg', 'rus')