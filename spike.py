from PIL import Image, ImageDraw

DIMENSIONS = (500, 500)
CENTER = (250, 250)
RADIUS = 225
CENTER_CIRCLE_RADIUS = 100

# mask
mask_img = Image.new('L', DIMENSIONS, color=0)
mask_draw = ImageDraw.Draw(mask_img)
mask_draw.ellipse((CENTER[0] - RADIUS, CENTER[1] - RADIUS, CENTER[0]
                   + RADIUS, CENTER[1] + RADIUS), fill=255)

# center circle mask
center_circle_mask_size = (CENTER_CIRCLE_RADIUS * 2, CENTER_CIRCLE_RADIUS * 2)
center_circle_mask_img = Image.new('L', center_circle_mask_size, color=0)
center_circle_mask_draw = ImageDraw.Draw(center_circle_mask_img)
center_circle_mask_draw.ellipse((0, 0) + center_circle_mask_size, fill=255)

center_circle_img = Image.open("images/joy_jc.png")
spinner_img = Image.new('RGB', DIMENSIONS, color=(0, 0, 0))
spinner_img.putalpha(mask_img)
center_circle_img.putalpha(center_circle_mask_img)
spinner_img.paste(center_circle_img, (
    int((DIMENSIONS[0] - CENTER_CIRCLE_RADIUS * 2) / 2), int((DIMENSIONS[1] - CENTER_CIRCLE_RADIUS * 2) /
                                                             2)), center_circle_img)
spinner_img.save("spike_output.png")
