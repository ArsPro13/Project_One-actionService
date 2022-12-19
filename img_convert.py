from fpdf import FPDF
import numpy as np
from PIL import Image


def write_the_instruction(path, new_img, basic_colors, pixel_size):
    fpdf = FPDF()
    fpdf.add_page()
    fpdf.set_font("Arial", 'B', size=20)
    fpdf.cell(0, 10, "Instruction", ln=True, align='C')
    fpdf.set_font("Arial", size=16)
    for x in list(basic_colors.values()):
        fpdf.cell(0, 10, f"{x[0]}: {x[1]}", ln=True)
    fpdf.image(path, x=15, y=105, w=90)
    fpdf.image("output.png", x=115, y=105, w=90)
    width, height = new_img.size
    for i in range(0, width, 30 * pixel_size):
        for j in range(0, height, 40 * pixel_size):
            fpdf.add_page()
            fpdf.cell(0, 15,
                      f"Rectange ({i // pixel_size}, {j // pixel_size}) - ({min(30 + i // pixel_size, width)}, {min(40 + j // pixel_size, height)})",
                      align='C')
            for x in range(0, 30 * pixel_size, pixel_size):
                for y in range(0, 40 * pixel_size, pixel_size):
                    if (x + i < width) and (y + j < height):
                        r, g, b = new_img.getpixel((x + i, y + j))
                        fpdf.set_fill_color(r, g, b)
                        fpdf.ellipse((x // pixel_size) * 6 + 15, (y // pixel_size) * 6 + 25, 5, 5, "DF")
    fpdf.output(f"{path[:-4]}_instruction.pdf")
    return f"{path[:-4]}_instruction.pdf"


def fs_dither(img, nc):
    # Floyd-Steinberg dither the image into a palette with nc colours per channel.
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
