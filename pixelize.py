from PIL import Image
from fpdf import FPDF


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
    x = [dist(k, pix) for k in b_colors.keys()]
    return list(b_colors.keys())[x.index(min(x))]


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 20)
        self.cell(0, 10, "Intruction", ln=True, align='C')


# main service funtion
def pixelize(im, pix_size, basic_colors):
    fpdf = PDF('P', 'mm', 'Letter')
    fpdf.add_page()
    instr = {}
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
            color = change(av_arifm(colors), basic_colors)
            if color in instr:
                instr[color][0].append((i // pix_size, j // pix_size))
                instr[color][1] += 1
            else:
                instr[color] = [[], 0]
            for point in points.keys():
                res.putpixel(point, color)
    for x in instr.keys():
        fpdf.set_font("Arial", size=16)
        fpdf.cell(0, 10, f"{basic_colors[x]}: {instr[x][1]}", ln=True)
    for x in instr.keys():
        fpdf.set_font("Arial", 'B', size=16)
        fpdf.cell(0, 10, f"{basic_colors[x]} squares are:", ln=True, align='C')
        fpdf.set_font("Arial", size=16)
        fpdf.multi_cell(0, 20, f"{str((instr[x][0]))[1:-1]}")
    fpdf.output("output.pdf")
    # res.show()
    return res


# starts the process
def process():
    image = Image.open("img.jpg")  # choose the image
    pixel_size = 20  # set pixel_size
    basic_colors = {(0, 0, 0): "Black", (255, 255, 255): "White", (255, 0, 0): "Red", (255, 255, 0): "Yellow",
                    (0, 255, 0): "Green", (0, 255, 255): "Heaven", (0, 0, 255): "Blue",
                    (255, 0, 255): "Violet"}  # in work
    new_image = pixelize(image, pixel_size, basic_colors)
    new_image.save("output.jpg")


process()
