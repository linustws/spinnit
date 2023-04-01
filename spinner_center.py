# Small circle at the center of the spinwheel
from PIL import Image
from PIL import ImageDraw

import SpinnerGifMaker

circle_radius = 20
circle_img = Image.new('RGBA', SpinnerGifMaker.DIMENSIONS, (0, 0, 0, 0))
draw = ImageDraw.Draw(circle_img)
draw.ellipse(
    (SpinnerGifMaker.CENTER[0] - circle_radius, SpinnerGifMaker.CENTER[1] - circle_radius,
     SpinnerGifMaker.CENTER[0] + circle_radius, SpinnerGifMaker.CENTER[1] +
     circle_radius),
    fill='black', outline='black')
circle_img.save('spinner_center.png')
