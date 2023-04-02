from PIL import Image
from PIL import ImageDraw

import SpinnerGifMaker

# mask
mask_img = Image.new('L', SpinnerGifMaker.DIMENSIONS, color=0)
mask_draw = ImageDraw.Draw(mask_img)
mask_draw.ellipse((SpinnerGifMaker.CENTER[0] - SpinnerGifMaker.RADIUS, SpinnerGifMaker.CENTER[1] - SpinnerGifMaker.RADIUS, SpinnerGifMaker.CENTER[0]
                   + SpinnerGifMaker.RADIUS, SpinnerGifMaker.CENTER[1] + SpinnerGifMaker.RADIUS), fill=255)
mask_img.save('mask.png')

triangle_img = Image.new('RGBA', SpinnerGifMaker.DIMENSIONSZ, (0, 0, 0, 0))
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

# spinner center
circle_radius = 20
circle_img = Image.new('RGBA', SpinnerGifMaker.DIMENSIONS, (0, 0, 0, 0))
draw = ImageDraw.Draw(circle_img)
draw.ellipse(
    (SpinnerGifMaker.CENTER[0] - circle_radius, SpinnerGifMaker.CENTER[1] - circle_radius,
     SpinnerGifMaker.CENTER[0] + circle_radius, SpinnerGifMaker.CENTER[1] +
     circle_radius),
    fill='black', outline='black')
circle_img.save('spinner_center.png')
