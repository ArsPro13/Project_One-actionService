import img_convert
from PIL import Image


def process(path):  # path to image in input
    image = Image.open(path)
    pixel_size = 4  # set pixel_size
    number_of_pins = 360  # set how many pins on lines (multiplied by pixel_size)
    # new_image = image.resize((number_of_pins, number_of_pins * image.size[1] // image.size[0]))
    basic_colors = {(0, 0, 0): ["Black", 0], (255, 255, 0): ["Yellow", 0], (0, 255, 255): ["Cyan", 0],
                    (255, 0, 255): ["Magenta", 0], (255, 0, 0): ["Red", 0], (0, 255, 0): ["Green", 0],
                    (0, 0, 255): ["Blue", 0], (255, 255, 255): ["White", 0]}  # palette
    new_image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size))
    new_image = img_convert.fs_dither(new_image, 2)
    new_image = img_convert.back_to_size(new_image, pixel_size)
    # new_image.show()
    new_image.save("output.png")
    img_convert.count_pixels(new_image, basic_colors, pixel_size)
    new_path = img_convert.write_the_instruction(path, new_image, basic_colors, pixel_size)
    return new_path
