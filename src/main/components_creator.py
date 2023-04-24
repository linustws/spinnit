from PIL import Image
from PIL import ImageDraw


def create_images(spinner_dimensions, spinner_center, spinner_radius, center_circle_radius):
    # mask
    mask_img = Image.new('L', spinner_dimensions, color=0)
    mask_draw = ImageDraw.Draw(mask_img)
    mask_draw.ellipse((spinner_center[0] - spinner_radius, spinner_center[1] - spinner_radius, spinner_center[0]
                       + spinner_radius, spinner_center[1] + spinner_radius), fill=255)
    mask_img.save('mask.png')

    # center circle mask
    center_circle_mask_size = (center_circle_radius * 2, center_circle_radius * 2)
    center_circle_mask_img = Image.new('L', center_circle_mask_size, color=0)
    center_circle_mask_draw = ImageDraw.Draw(center_circle_mask_img)
    center_circle_mask_draw.ellipse((0, 0) + center_circle_mask_size, fill=255)
    center_circle_mask_img.save('center_circle_mask.png')

    # circle outline
    circle_outline_img = Image.new('RGBA', spinner_dimensions, (0, 0, 0, 0))
    circle_outline_draw = ImageDraw.Draw(circle_outline_img)
    circle_outline_draw.ellipse((0, 0) + (spinner_radius * 2, spinner_radius * 2),
                                fill=None, outline='black')
    circle_outline_img.save('circle_outline.png')

    # center circle outline
    center_circle_outline_img = Image.new('RGBA', spinner_dimensions, (0, 0, 0, 0))
    center_circle_outline_draw = ImageDraw.Draw(center_circle_outline_img)
    center_circle_outline_draw.ellipse((0, 0) + center_circle_mask_size,
                                fill=None, outline=(0, 0, 0, 255))
    center_circle_outline_img.save('center_circle_outline.png')

    # Triangle pointer
    triangle_img = Image.new('RGBA', spinner_dimensions, (0, 0, 0, 0))
    draw = ImageDraw.Draw(triangle_img)
    triangle_height = 30
    triangle_base = 20
    triangle_top = (spinner_center[0], spinner_center[1] - spinner_radius + triangle_height)
    triangle_left = (spinner_center[0] - triangle_base / 2, spinner_center[1] - spinner_radius - 10)
    triangle_right = (
        spinner_center[0] + triangle_base / 2, spinner_center[1] - spinner_radius - 10)
    draw.polygon([triangle_top, triangle_left, triangle_right], fill='red', outline='black')
    triangle_img.save('triangle.png')
