import os

import pytesseract
import cv2
import numpy as np

def scan_image(name_image, language : str):
    if language == 'rus':
        language = 'rus+eng'
    image = cv2.imread(name_image)
    #image = normalizing(image)#нормализация изображения
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
    #image = remove_noise(image)#удаление шума
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)
    #image = gray(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #image = thresholding(image)#бинаризация
    ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    return pytesseract.image_to_string(image, lang=language)