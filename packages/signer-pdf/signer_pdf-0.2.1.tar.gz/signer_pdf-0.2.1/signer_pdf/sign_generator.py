# coding=utf-8
import io
from datetime import datetime

import pkg_resources
from PIL import Image, ImageDraw, ImageFont

WIDTH = 700
HEIGHT = 180
FONT_SIZE = 32
FONT = pkg_resources.resource_filename(__name__, 'resources/font.ttf')


def draw_date(draw, date):
    font = ImageFont.truetype(FONT, FONT_SIZE)
    draw.text((20, 110), u"Дата и время: " + date.strftime("%Y-%m-%d %H:%M:%S"), font=font, fill=(0, 0, 0))


def draw_longstring(draw, name, position):
    font = ImageFont.truetype(FONT, FONT_SIZE)

    font_size = FONT_SIZE
    if font.getsize(name)[0] > WIDTH:
        txt_length = font.getsize(name)[0]
        font_size *= WIDTH / txt_length
        font = ImageFont.truetype(FONT, int(font_size) - 1 if font_size > 2 else int(font_size))

    draw.text(position, name, font=font, fill=(0, 0, 0))


def generate_img(name: str, date: datetime, a_hash: str, position: str) -> io.BytesIO:
    sign_img = Image.new('RGBA', (WIDTH, HEIGHT), color=(255, 255, 255, 0))

    d = ImageDraw.Draw(sign_img)
    draw_longstring(d, u"Подписано электронной подписью:", (20, 20))
    draw_longstring(d, name, (20, 50))
    if position != "":
        draw_longstring(d, u"Должность: " + position, (20, 80))
    draw_date(d, date)
    draw_longstring(d, a_hash, (20, 140))

    sign_img_bytes = io.BytesIO()
    sign_img.save(sign_img_bytes, format='png')
    sign_img_bytes.seek(0)

    return sign_img_bytes
