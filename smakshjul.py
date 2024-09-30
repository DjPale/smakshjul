from PIL import Image, ImageDraw, ImageFont
import csv 
import math

def read_data(fname):
    with open(fname, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        data = []

        skipped = False
        for row in reader:
            if not skipped:
                skipped = True
            else:
                data.append(row)

    return data


def gen_rotated_text(text: str, font: ImageFont, angle: float, anchor: str = "la"):
    img = Image.new('RGBA', (150, 50), color = (0, 0, 255, 100))
    draw = ImageDraw.Draw(img)
    tl = draw.textlength(text, font)
    #x = (150 / 2) - (tl / 2)
    #y = (50 / 2) - ( 10 / 2)
    x = 0
    y = 0
    draw.text((x, y), text, font = font, anchor = anchor)

    return img.rotate(angle, expand = True)
    
            
def create_image(data, rect_size):
    width = rect_size
    height = rect_size

    outer_r = (rect_size / 2) - 100
    # - (rect_size / 60 * 10)

    font_sz = rect_size / 60

    img = Image.new(mode = 'RGBA', size = (width, height))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font = 'ClearSans-Bold.ttf', size = font_sz)
    
    x = 0
    y = 0

    angle_step = 360.0 / len(data)
    angle = 180.0

    angle_ofs = 180.0
    anchor = "la"

    for line in data:       
        x = (width / 2) + (outer_r * math.sin(math.radians(angle))) + font_sz / 2
        y = (height / 2) + (outer_r * math.cos(math.radians(angle))) + font_sz / 2

        if angle <= 0.0:
            angle_ofs = 0.0
            anchor = "la"

        text_angle = angle + 90.0 + angle_ofs
        text_img = gen_rotated_text(line[0], font, text_angle, anchor = anchor)

        w = text_img.width
        h = text_img.height
        h_w = text_img.width / 2
        h_h = text_img.height / 2
        
        r_a = math.radians(text_angle)

        x_ofs = 0
        y_ofs = 0

        img.paste(text_img, (int(x + x_ofs), int(y + y_ofs)), text_img)

        print(angle, x, y, text_img.width, text_img.height)

        draw.circle((x, y), 2)

        angle -= angle_step

    img.show()

data = read_data('smakshjul-data-small.csv')

create_image(data, 800)
