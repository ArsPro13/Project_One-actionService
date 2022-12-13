from PIL import Image


# following subfunctions are made for different types of picture's modifying
def av_geom(colors):  # colored
    sm0 = 1
    sm1 = 1
    sm2 = 1
    for x in colors:
        sm0 *= x[0] if x[0] else 1
        sm1 *= x[1] if x[1] else 1
        sm2 *= x[2] if x[2] else 1
    return (int((sm0) ** (1 / len(colors))), int((sm1) ** (1 / len(colors))), int((sm2) ** (1 / len(colors))))


def av_arifm(colors):
    sm0 = 0
    sm1 = 0
    sm2 = 0
    for x in colors:
        sm0 += x[0]
        sm1 += x[1]
        sm2 += x[2]
    return (sm0 // len(colors), sm1 // len(colors), sm2 // len(colors))


def basic(colors):  # first variant
    return colors[len(colors) // 2]


# subfunctin for comparising
def dist(x1, x2):
    return (x1[2] - x2[2]) ** 2 + (x1[1] - x2[1]) ** 2 + (x1[0] - x2[0]) ** 2


def cosine_sqr(x1, x2):
    return (x1[0] * x2[0] + x1[1] * x2[1] + x1[2] * x2[2]) ** 2 / (dist(x1, (0, 0, 0)) * dist(x2, (0, 0, 0)))


# functions for changing cur_color to one of the basic's
def change(pix, b_colors):
    x = [dist(k, pix) for k in b_colors]
    return b_colors[x.index(min(x))]


def color_set(colors, basic_colors):
    color = change(av_arifm(colors), basic_colors)  # сhoose a version
    # color = basic(colors)
    return color


# main service funtion
def pixelize(im, pix_size, basic_colors):
    n, m = im.size[0], im.size[1]
    res = Image.new("RGB", (n, m), color=0)
    for i in range(0, n, pix_size):
        for j in range(0, m, pix_size):
            points = {}
            for x in range(pix_size):
                if i + x >= n:
                    break
                for y in range(pix_size):
                    if j + y >= m:
                        continue
                    points[(i + x, j + y)] = im.getpixel((i + x, j + y))
            colors = list(sorted(points.values()))
            color = color_set(colors, basic_colors)
            for point in points.keys():
                res.putpixel(point, color)
    res.show()
    return res


# function which generates the instructions for customer (soon)
def write_the_instructions(im, pixel_size):
    instr = {}
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pix = im.getpixel((i, j))
            if pix in instr:
                instr[pix] += 1
            else:
                instr[pix] = 1
    for x in instr.keys():
        instr[x] //= pixel_size ** 2
    return instr


# starts the process
def process():
    image = Image.open("img.jpg")  # choose the image
    pixel_size = 3  # set pixel_size
    basic_colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (255, 255, 0),
                    (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)] # in work
    new_image = pixelize(image, pixel_size, basic_colors)
    # the next is not ready now
    instructions = write_the_instructions(new_image, pixel_size)
    print(instructions)


process()
