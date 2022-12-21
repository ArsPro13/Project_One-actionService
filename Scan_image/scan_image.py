import os

import pytesseract
import cv2
import numpy as np

def remove_noise(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)


def normalizing(image):
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
    return image


def gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def thresholding(image):
    ret, im = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    return im


def scan_image(name_image, language):
    image = cv2.imread(name_image)
    image = normalizing(image)#нормализация изображения
    image = remove_noise(image)#удаление шума
    image = gray(image)
    image = thresholding(image)#бинаризация
    print(pytesseract.image_to_string(image, lang=language))


def scan_images(name_of_directory, language='eng'):
    for root, dirs, file_names in os.walk(name_of_directory):
        for file_name in file_names:
            if language == 'rus':
                language += '+eng'
            scan_image(name_of_directory + file_name, language)

scan_image('tests_rus/rus_photo1.jpg', 'rus')