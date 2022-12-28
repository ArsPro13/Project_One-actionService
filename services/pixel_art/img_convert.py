from fpdf import FPDF
import numpy as np
from PIL import Image


def write_the_instruction(path, dir_name, new_img, basic_colors, pixel_size):
    fpdf = FPDF()
    fpdf.add_page()
    fpdf.set_font("Arial", 'B', size=20)
    fpdf.cell(0, 10, "Pin art", ln=True, align='C')
    fpdf.cell(0, 10, "instruction", ln=True, align='C')
    fpdf.set_font("Arial", size=16)
    for x in range(4):
        fpdf.text(65, 10 * x + 50, f"{list(basic_colors.values())[x + 4][0]}: {list(basic_colors.values())[x + 4][1]}")
        fpdf.text(110, 10 * x + 50, f"{list(basic_colors.values())[x][0]}: {list(basic_colors.values())[x][1]}")
    width, height = new_img.size
    fpdf.text(65, 95, f"Final size: {int(0.5 * width // pixel_size)}*{int(0.5 * height // pixel_size)} centimetres")
    fpdf.image(path, x=10, y=130, w=90)
    fpdf.image(f"{dir_name}/output.png", x=110, y=130, w=90)
    fpdf.add_page()
    k = 0
    fpdf.set_font("Arial", 'B', size=20)
    fpdf.cell(0, 10, "Fragmentation", ln=True, align='C')
    fpdf.set_font("Arial", size=10)
    for i in range(0, width, 30 * pixel_size):
        for j in range(0, height, 40 * pixel_size):
            k += 1
            a, b = min(30 * pixel_size + i, width) * 190 / width, min(40 * pixel_size + j, height) * 190 / width
            fpdf.rect(10, 25, a, b)
            x = (min(30 * pixel_size + i, width) - i) / 2
            y = (min(40 * pixel_size + j, height) - j) / 2
            fpdf.text(8 + a - (190 * x / width), 26 + b - (190 * y / width), str(k))
    fpdf.set_font("Arial", size=18)
    k = 0
    for i in range(0, width, 30 * pixel_size):
        for j in range(0, height, 40 * pixel_size):
            k += 1
            fpdf.add_page()
            fpdf.cell(0, 15, f"Rectangle {k}", align='C')
            for x in range(0, 30 * pixel_size, pixel_size):
                for y in range(0, 40 * pixel_size, pixel_size):
                    if (x + i < width) and (y + j < height):
                        r, g, b = new_img.getpixel((x + i, y + j))
                        fpdf.set_fill_color(r, g, b)
                        fpdf.ellipse((x // pixel_size) * 6 + 15, (y // pixel_size) * 6 + 25, 5, 5, "DF")
    fpdf.output(f"{dir_name}/instruction.pdf")
    return f"{dir_name}/instruction.pdf"


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
        x[1] //= (pixel_size ** 2)
