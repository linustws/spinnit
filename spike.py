from PIL import Image, ImageDraw

DIMENSIONS = (500, 500)
CENTER = (250, 250)
RADIUS = 225
CENTER_CIRCLE_RADIUS = 100

# Limit the colors in the image to 254, so that there are 2 colors left, 1 for transparency, and 1 for the black circle
center_circle_img = Image.open("images/joy/joy_jc.png").convert("RGB").quantize(254)

# Find a color that isn't used yet to be the transparent background. That is the first color
for i in range(255):
    color = (i, 255, 255)
    if color not in center_circle_img.palette.colors:
        transparent_background = center_circle_img.palette.getcolor(color)
        break

spinner_img = Image.new("P", DIMENSIONS, transparent_background)
spinner_img.info["transparency"] = transparent_background
spinner_img.paste(center_circle_img, (int((DIMENSIONS[0] - CENTER_CIRCLE_RADIUS * 2) / 2), int((DIMENSIONS[1] - CENTER_CIRCLE_RADIUS * 2) / 2)))
spinner_img.putpalette(center_circle_img.palette)

# mask
mask_img = Image.new('L', DIMENSIONS)
mask_draw = ImageDraw.Draw(mask_img)
# Calling spinner_img.palette.getcolor((0, 0, 0)) allocates the second color to be black
mask_draw.ellipse((CENTER[0] - RADIUS, CENTER[1] - RADIUS, CENTER[0] + RADIUS, CENTER[1] + RADIUS), fill=spinner_img.palette.getcolor((0, 0, 0)))
mask_draw.ellipse((CENTER[0] - CENTER_CIRCLE_RADIUS, CENTER[1] - CENTER_CIRCLE_RADIUS, CENTER[0] + CENTER_CIRCLE_RADIUS, CENTER[1] + CENTER_CIRCLE_RADIUS), fill=0)

spinner_img.paste(mask_img, mask=mask_img)
spinner_img.save("spike_output.gif")