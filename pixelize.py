from fpdf import FPDF
import numpy as np
from PIL import Image


def fs_dither(img, nc):
    # Floyd-Steinberg dither the image into a palette with color_number colours per
    # channel.
    arr = np.array(img, float) / 255
    width, height = img.size
    for i in range(height):
        for j in range(width):
            old_val = arr[i, j].copy()
            new_val = np.round(old_val * (nc - 1)) / (nc - 1)
            arr[i, j] = new_val
            err = old_val - new_val
            if j < width - 1:
                arr[i, j + 1] += err * 7 / 16
            if i < height - 1:
                if j > 0:
                    arr[i + 1, j - 1] += err * 3 / 16
                arr[i + 1, j] += err * 5 / 16
                if j < width - 1:
                    arr[i + 1, j + 1] += err / 16
    carr = np.array(arr / np.max(arr, axis=(0, 1)) * 255, dtype=np.uint8)
    return Image.fromarray(carr)


def back_to_size(img, pix_size):
    width, height = img.size
    new = Image.new("RGB", (width * pix_size, height * pix_size))
    for i in range(height * pix_size):
        for j in range(width * pix_size):
            new.putpixel((j, i), img.getpixel((j // pix_size, i // pix_size)))
    return new


def count_pixels(img, basic_colors, pixel_size):
    width, height = img.size
    for i in range(height):
        for j in range(width):
            basic_colors[img.getpixel((j, i))][1] += 1
    for x in list(basic_colors.values()):
        x[1] //= pixel_size ** 2


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', size=20)
        self.cell(0, 10, "Intruction", ln=True, align='C')


def write_the_instruction(path, new_img, basic_colors):
    fpdf = PDF('P', 'mm', 'Letter')
    fpdf.set_font("Arial", size=16)
    fpdf.add_page()
    for x in list(basic_colors.values()):
        fpdf.cell(0, 10, f"{x[0]}: {x[1]}", ln=True)
    fpdf.image(path, x=15, y=105, w=90)
    fpdf.image("output.png", x=115, y=105, w=90)
    fpdf.output(f"{path[:-4]}_instruction.pdf")
    return f"{path[:-4]}_instruction.pdf"


def process():
    path = input()  # path to image input
    image = Image.open(path)
    pixel_size = 4  # set pixel_size
    number_of_pins = 360  # set how many pins on lines (multiplied by pixel_size)
    # new_image = image.resize((number_of_pins, number_of_pins * image.size[1] // image.size[0]))
    basic_colors = {(0, 0, 0): ["Black", 0], (255, 255, 0): ["Yellow", 0], (0, 255, 255): ["Cyan", 0],
                    (255, 0, 255): ["Magenta", 0], (255, 0, 0): ["Red", 0], (0, 255, 0): ["Green", 0],
                    (0, 0, 255): ["Blue", 0], (255, 255, 255): ["White", 0]}  # palette
    new_image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size))
    new_image = fs_dither(new_image, 2)
    new_image = back_to_size(new_image, pixel_size)
    # new_image.show()
    new_image.save("output.png")
    count_pixels(new_image, basic_colors, pixel_size)
    return write_the_instruction(path, new_image, basic_colors)


process()
