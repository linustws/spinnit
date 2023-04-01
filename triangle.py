from PIL import Image
from PIL import ImageDraw

import SpinnerGifMaker

triangle_img = Image.new('RGBA', SpinnerGifMaker.DIMENSIONS, (0, 0, 0, 0))
draw = ImageDraw.Draw(triangle_img)

# Triangle pointer
triangle_height = 30
triangle_base = 20
triangle_top = (SpinnerGifMaker.CENTER[0], SpinnerGifMaker.CENTER[1] - SpinnerGifMaker.RADIUS + triangle_height)
triangle_left = (SpinnerGifMaker.CENTER[0] - triangle_base / 2, SpinnerGifMaker.CENTER[1] - SpinnerGifMaker.RADIUS - 10)
triangle_right = (
    SpinnerGifMaker.CENTER[0] + triangle_base / 2, SpinnerGifMaker.CENTER[1] - SpinnerGifMaker.RADIUS - 10)
draw.polygon([triangle_top, triangle_left, triangle_right], fill='red', outline='black')
triangle_img.save('triangle.png')
