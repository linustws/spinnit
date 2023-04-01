# Create mask for spinwheel image
from PIL import Image
from PIL import ImageDraw

import SpinnerGifMaker

mask_img = Image.new('L', SpinnerGifMaker.DIMENSIONS, color=0)
mask_draw = ImageDraw.Draw(mask_img)
mask_draw.ellipse((SpinnerGifMaker.CENTER[0] - SpinnerGifMaker.RADIUS, SpinnerGifMaker.CENTER[1] - SpinnerGifMaker.RADIUS, SpinnerGifMaker.CENTER[0]
                   + SpinnerGifMaker.RADIUS, SpinnerGifMaker.CENTER[1] + SpinnerGifMaker.RADIUS), fill=255)
mask_img.save('mask.png')
