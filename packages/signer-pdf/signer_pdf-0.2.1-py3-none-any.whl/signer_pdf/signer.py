import io

import fitz

import signer_pdf.sign_generator as sign_generator

RECT_WIDTH = 256
RECT_HEIGHT = 64


def sign(name, date, a_hash, position, in_file, right_top=False):
    document: fitz.Document = fitz.open(in_file)
    page = document[0]

    if right_top:
        top_right_point = page.rect.top_right
        img_rect = fitz.Rect(
            top_right_point[0] - RECT_WIDTH,
            0,
            top_right_point[0],
            top_right_point[1] + RECT_HEIGHT
        )
    else:
        bottom_left_point = page.rect.bottom_left
        img_rect = fitz.Rect(
            0,
            bottom_left_point[1] - RECT_HEIGHT,
            RECT_WIDTH,
            bottom_left_point[1]
        )

    sign_img = sign_generator.generate_img(name, date, a_hash, position)
    page.insertImage(img_rect, stream=sign_img)

    return io.BytesIO(document.write())
