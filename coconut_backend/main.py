from PIL import Image, ImageDraw, ImageFont

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def postcard_maker(name, picline, pic_num):
    if 1 > pic_num > 3:
        raise ValueError('pic_num must be between 1 and 3')

    im_file = Image.open(
        f'coconut_backend/images/coconut_postcard_{pic_num}.png')
    draw = ImageDraw.Draw(im_file)
    font = ImageFont.truetype('coconut_backend/fonts/DavysCrappyWrit.ttf', 75)
    width, height = im_file.size

    to_font = ImageFont.truetype(
        'coconut_backend/fonts/DavysCrappyWrit.ttf', 50)
    draw.text((200, height // 2 - 50),
              picline.replace("’", "'"), (0, 0, 0), font=font)

    draw.text((200, height // 2 - 120),
              f"To {name},", (0, 0, 0), font=to_font)

    return im_file


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/postcard')
def postcard(name: str, picline: str, gender: str):
    if gender.strip().lower() == "male":
        pic_num = 2
    else:
        pic_num = 1

    im_file = postcard_maker(name, picline, pic_num)
    
    im = BytesIO()
    im_file.save(im, 'PNG')
    im.seek(0)
    return StreamingResponse(im, media_type='image/png')


if __name__ == '__main__':
    app.run()
