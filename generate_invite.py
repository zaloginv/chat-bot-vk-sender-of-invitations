from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = 'files/invite.png'
FONT_PATH = 'files/font_mt.ttf'
FONT_SIZE = 30

BLACK_COLOR = (0, 0, 0, 255)
NAME_OFFSET = (551, 350)
EMAIL_OFFSET = (525, 390)

def generate_invite(name, email):
    base = Image.open(TEMPLATE_PATH).convert('RGBA')
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, name, font=font, fill=BLACK_COLOR)
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK_COLOR)

    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file