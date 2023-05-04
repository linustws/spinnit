import math
import os
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from components_creator import create_images
from logger import Logger

this_dir = os.path.dirname(__file__)
logger_rel_path = '../../spinnit.log'
logger_abs_path = os.path.join(this_dir, logger_rel_path)
spinner_logger = Logger('spinner', logger_abs_path)
components_abs_path = os.path.join(this_dir, '../../assets/components/')
fonts_abs_path = os.path.join(this_dir, '../../assets/fonts/')
general_img_abs_path = os.path.join(this_dir, '../../assets/images/general/')
special_img_abs_path = os.path.join(this_dir, '../../assets/images/special/')

DIMENSIONS = (500, 500)
CENTER = (250, 250)
RADIUS = 225
DIAMETER = RADIUS * 2
CENTER_CIRCLE_RADIUS = 100
NUM_SPIN_FRAMES = 100
NUM_BLINK_FRAMES = 50
NUM_TOTAL_FRAMES = NUM_SPIN_FRAMES + NUM_BLINK_FRAMES
# frame durations
DURATIONS = [1000, 300, 200, 130, 80, 60, 40, 30, 25, 20] \
            + [20 for _ in range(NUM_SPIN_FRAMES - 20)] + [20, 25, 30, 40, 60, 80, 130, 200, 300, 1000] \
            + [100 for _ in range(NUM_BLINK_FRAMES)]  # fastest 20
ANGLES = [0, -2, -5, -10, -15, -20, -30, -50, -70, -100] + \
         [i * -150 - 150 for i in range(int((NUM_SPIN_FRAMES - 20) / 2))] + \
         [i * -150 + 6000 for i in range(int((NUM_SPIN_FRAMES - 20) / 2))] + \
         [100, 70, 50, 30, 20, 15, 10, 5, 2, 0]

# import components
try:
    MASK_IMG = Image.open(components_abs_path + 'mask.png')
    CENTER_CIRCLE_MASK_IMG = Image.open(components_abs_path + 'center_circle_mask.png')
    CIRCLE_OUTLINE_IMG = Image.open(components_abs_path + 'circle_outline.png')
    CENTER_CIRCLE_OUTLINE_IMG = Image.open(components_abs_path + 'center_circle_outline.png')
    TRIANGLE_IMG = Image.open(components_abs_path + 'triangle.png')
except FileNotFoundError as e:
    create_images(DIMENSIONS, CENTER, RADIUS, CENTER_CIRCLE_RADIUS)
    MASK_IMG = Image.open(components_abs_path + 'mask.png')
    CENTER_CIRCLE_MASK_IMG = Image.open(components_abs_path + 'center_circle_mask.png')
    CIRCLE_OUTLINE_IMG = Image.open(components_abs_path + 'circle_outline.png')
    CENTER_CIRCLE_OUTLINE_IMG = Image.open(components_abs_path + 'center_circle_outline.png')
    TRIANGLE_IMG = Image.open(components_abs_path + 'triangle.png')
NUM_BG_IMG_COLORS = 16
NUM_SPINNER_IMG_COLORS = 10

# 500 x 500 pic
BG_IMG_GENERAL_QUANTIZED = Image.open(general_img_abs_path + 'bg/starry_night.png').resize(
    (500, 500)).convert('RGB').quantize(NUM_BG_IMG_COLORS)
# 200 x 200 pic
CENTER_CIRCLE_COVER_IMG_GENERAL = Image.open(general_img_abs_path + 'cover/cat.png').resize((200, 200))
# quantize colors minus 1 to reserve color for triangle
CENTER_CIRCLE_COVER_IMG_GENERAL_QUANTIZED = CENTER_CIRCLE_COVER_IMG_GENERAL.copy().convert('RGB').quantize(
    256 - NUM_BG_IMG_COLORS - NUM_SPINNER_IMG_COLORS - 1)
REVEAL_GENERAL_FILE_PATH = general_img_abs_path + 'reveal'
REVEAL_GENERAL_FILE_LIST = os.listdir(REVEAL_GENERAL_FILE_PATH)

try:
    BG_IMG_SPECIAL_QUANTIZED = Image.open(special_img_abs_path + 'bg/strawberry.png').resize(
        (500, 500)).convert('RGB').quantize(NUM_BG_IMG_COLORS)
    CENTER_CIRCLE_COVER_IMG_SPECIAL = Image.open(special_img_abs_path + 'cover/kuromi.png').resize(
        (200, 200))
    CENTER_CIRCLE_COVER_IMG_SPECIAL_QUANTIZED = CENTER_CIRCLE_COVER_IMG_SPECIAL.copy().convert('RGB').quantize(
        256 - NUM_BG_IMG_COLORS - NUM_SPINNER_IMG_COLORS - 1)
    REVEAL_SPECIAL_FILE_PATH = special_img_abs_path + 'reveal'
    REVEAL_SPECIAL_FILE_LIST = os.listdir(REVEAL_SPECIAL_FILE_PATH)
except FileNotFoundError as e:
    spinner_logger.log('warning', "Special images not found! Will respond to all using general images.")
    BG_IMG_SPECIAL_QUANTIZED = BG_IMG_GENERAL_QUANTIZED
    REVEAL_SPECIAL_FILE_PATH = REVEAL_GENERAL_FILE_PATH
    REVEAL_SPECIAL_FILE_LIST = REVEAL_GENERAL_FILE_LIST
    CENTER_CIRCLE_COVER_IMG_SPECIAL = CENTER_CIRCLE_COVER_IMG_GENERAL
    CENTER_CIRCLE_COVER_IMG_SPECIAL_QUANTIZED = CENTER_CIRCLE_COVER_IMG_GENERAL_QUANTIZED

CIRCLE_OUTLINE_IMG_QUANTIZED = CIRCLE_OUTLINE_IMG.convert('RGB').quantize(2)
CENTER_CIRCLE_OUTLINE_IMG_QUANTIZED = CENTER_CIRCLE_OUTLINE_IMG.convert('RGB').quantize(2)
TRIANGLE_IMG_QUANTIZED = TRIANGLE_IMG.convert('RGB').quantize(2)
PASTEL_COLORS = [(220, 214, 255), (214, 240, 255), (222, 255, 239), (255, 250, 240), (255, 237, 237),
                 (255, 222, 222), (247, 246, 207), (182, 216, 242), (244, 207, 223), (87, 132, 186),
                 (154, 200, 235), (204, 212, 191), (231, 203, 169), (238, 186, 178), (245, 243, 231),
                 (245, 226, 228), (245, 191, 210), (229, 219, 156), (208, 188, 172), (190, 180, 197),
                 (230, 165, 126), (33, 139, 130), (154, 217, 219), (229, 219, 217), (152, 212, 187),
                 (235, 150, 170), (198, 201, 208), (229, 179, 187), (196, 116, 130), (249, 150, 139),
                 (118, 205, 205), (123, 146, 170), (228, 206, 224), (161, 93, 152), (220, 130, 143),
                 (247, 206, 118), (140, 115, 134), (156, 147, 89), (165, 114, 131), (232, 213, 149)]


class Spinner:

    def __init__(self, chat_id, options, is_special):
        # start = time.time()
        random.shuffle(options)
        self.options = options
        if is_special:
            self.bg_img = BG_IMG_SPECIAL_QUANTIZED
            self.center_circle_cover_img = CENTER_CIRCLE_COVER_IMG_SPECIAL
            self.center_circle_cover_img_quantized = CENTER_CIRCLE_COVER_IMG_SPECIAL_QUANTIZED
            folder_path = REVEAL_SPECIAL_FILE_PATH
            file_list = REVEAL_SPECIAL_FILE_LIST
        else:
            self.bg_img = BG_IMG_GENERAL_QUANTIZED
            self.center_circle_cover_img = CENTER_CIRCLE_COVER_IMG_GENERAL
            self.center_circle_cover_img_quantized = CENTER_CIRCLE_COVER_IMG_GENERAL_QUANTIZED
            folder_path = REVEAL_GENERAL_FILE_PATH
            file_list = REVEAL_GENERAL_FILE_LIST
        image_list = [filename for filename in file_list if filename.endswith(('.png', '.jpg', '.jpeg'))]
        random_image = random.choice(image_list)
        image_path = os.path.join(folder_path, random_image)
        # 200 x 200 pic
        self.center_circle_img = Image.open(image_path).resize((200, 200))
        # self.center_circle_img = Image.open('images/reveal/joy_jc.png')
        # quantize colors minus 1 to reserve color for triangle
        self.center_circle_img_with_triangle_quantized = self.center_circle_img.convert('RGB').quantize(
            256 - NUM_BG_IMG_COLORS - NUM_SPINNER_IMG_COLORS - 1)
        self.center_circle_img_no_triangle_quantized = self.center_circle_img.convert('RGB').quantize(
            256 - NUM_BG_IMG_COLORS - NUM_SPINNER_IMG_COLORS)
        self.colors = random.sample(PASTEL_COLORS, len(options))
        # start and end at unpredictable positions
        start_offset = random.randint(0, 359)
        end_offset = random.randint(0, 359)
        self.spinner_angles = [angle - start_offset for angle in ANGLES[:50]] + [angle - end_offset for angle in
                                                                                 ANGLES[50:]]
        self.image_angles = ANGLES
        self.stop_frame_no_triangle = None
        self.stop_frame_with_triangle = None
        self.gif_path = os.path.join(this_dir, f"{chat_id}.gif")

        bg_img, spinner_img = self.prepare()

        frame_list = []
        for i in range(NUM_TOTAL_FRAMES):
            # print(f'frame {i}')
            frame = self.getSpinnerFrame(bg_img.copy(), spinner_img, i)
            frame_list.append(frame)
        frame_list[0].save(self.gif_path, format='GIF', append_images=frame_list[1:], save_all=True,
                           duration=DURATIONS, disposal=2, loop=0)
        # end = time.time()
        # print(f'time taken no mp unposterised: {end - start} seconds')

    def paste(self, bg_img, im, box=None, mask=None):
        # to combine one P image with another
        # add all of the new colors to the palette of the first image
        remap = [0] * 256
        for color, i in im.palette.colors.items():
            remap[i] = bg_img.palette.getcolor(color)
        # then update the palette indexes in the new image
        im = im.point(remap)
        # and paste
        bg_img.paste(im, box, mask)

    def prepare(self):
        # 16 colors
        bg_img = self.bg_img
        spinner_img = Image.new('RGB', DIMENSIONS, color=(0, 0, 0))
        # add color pie slices
        spinner_draw = ImageDraw.Draw(spinner_img, 'RGBA')
        num_sectors = len(self.options)
        for i, option in enumerate(self.options):
            start_angle = i * (360 / num_sectors)
            end_angle = (i + 1) * (360 / num_sectors)
            color = self.colors[i]
            fill = (255,)
            # draw pie slices
            spinner_draw.pieslice(xy=((CENTER[0] - RADIUS, CENTER[1] - RADIUS), (CENTER[0] + RADIUS, CENTER[1] +
                                                                                 RADIUS)),
                                  start=start_angle,
                                  end=end_angle, fill=color + fill, outline='black')

            # add text options
            font = ImageFont.truetype(fonts_abs_path + 'arial.ttf', 30)
            _, _, text_width, text_height = spinner_draw.textbbox((0, 0), option, font=font, anchor='lt')
            sector_center_angle = (start_angle + end_angle) / 2
            sector_center_x = CENTER[0] + (RADIUS + CENTER_CIRCLE_RADIUS) * 0.5 * math.cos(sector_center_angle *
                                                                                           math.pi / 180)
            sector_center_y = CENTER[1] + (RADIUS + CENTER_CIRCLE_RADIUS) * 0.5 * math.sin(sector_center_angle *
                                                                                           math.pi / 180)
            text_angle = 180 - sector_center_angle
            text_img = Image.new('RGBA', (text_width, text_height), color=(0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_draw.text((0, 0), option, fill=(0, 0, 0), font=font, anchor='lt')
            text_img = text_img.rotate(text_angle, expand=True)
            text_width, text_height = text_img.size
            text_center_x = sector_center_x - text_width / 2
            text_center_y = sector_center_y - text_height / 2
            spinner_img.paste(text_img, (int(text_center_x), int(text_center_y)), text_img)
        # 10 colors
        spinner_img = spinner_img.quantize(NUM_SPINNER_IMG_COLORS)
        return bg_img, spinner_img

    def getSpinnerFrame(self, bg_img, spinner_img, frame_number):
        # return stored stop frames
        if self.stop_frame_no_triangle is not None and frame_number % 2 == 0:
            return self.stop_frame_no_triangle
        elif self.stop_frame_with_triangle is not None and frame_number % 2 == 1:
            return self.stop_frame_with_triangle
        # rotate
        elif frame_number < NUM_SPIN_FRAMES:
            spinner_img = spinner_img.rotate(self.spinner_angles[frame_number], center=CENTER)
            if frame_number < 40:
                center_circle_img = self.center_circle_cover_img_quantized.rotate(self.image_angles[frame_number],
                                                                                  center=(100, 100))
            elif frame_number >= 60:
                # with triangle quantized with 1 less color
                center_circle_img = self.center_circle_img_with_triangle_quantized.rotate(
                    self.image_angles[frame_number], center=(100, 100))
            else:
                # center circle cover mask that decreases in opacity
                center_circle_cover_mask_size = (CENTER_CIRCLE_RADIUS * 2, CENTER_CIRCLE_RADIUS * 2)
                center_circle_cover_mask_img = Image.new('L', center_circle_cover_mask_size, color=0)
                center_circle_cover_mask_draw = ImageDraw.Draw(center_circle_cover_mask_img)
                fill = int((20 - (frame_number - 40)) / 21 * 255)
                # print(frame_number, fill)
                center_circle_cover_mask_draw.ellipse((0, 0) + center_circle_cover_mask_size, fill=fill)

                # paste cover image
                center_circle_img = self.center_circle_img.copy()
                center_circle_img.paste(self.center_circle_cover_img, mask=center_circle_cover_mask_img)
                # quantize colors minus 1 to reserve color for triangle
                center_circle_img = center_circle_img.convert('RGB').quantize(
                    256 - NUM_BG_IMG_COLORS - NUM_SPINNER_IMG_COLORS - 1)
                center_circle_img = center_circle_img.rotate(self.image_angles[frame_number], center=(100, 100))

        # stop rotation
        else:
            spinner_img = spinner_img.rotate(self.spinner_angles[-1], center=CENTER)
            # with triangle quantized with 1 less color
            if frame_number % 2 == 1:
                center_circle_img = self.center_circle_img_with_triangle_quantized
            else:
                center_circle_img = self.center_circle_img_no_triangle_quantized
            center_circle_img = center_circle_img.rotate(self.image_angles[-1], center=(100, 100))

        self.paste(bg_img, spinner_img, (0, 0), MASK_IMG)

        # created outline image cos the spinner outline is quite wonky
        self.paste(bg_img, CIRCLE_OUTLINE_IMG_QUANTIZED,
                   (int((DIMENSIONS[0] - RADIUS * 2) / 2), int((DIMENSIONS[1] - RADIUS * 2) / 2)), CIRCLE_OUTLINE_IMG)

        self.paste(bg_img, center_circle_img, (
            int((DIMENSIONS[0] - CENTER_CIRCLE_RADIUS * 2) / 2), int((DIMENSIONS[1] - CENTER_CIRCLE_RADIUS * 2) /
                                                                     2)), CENTER_CIRCLE_MASK_IMG)
        # number of free colors left
        # colors_left = 256 - len(bg_img.palette.colors)
        # print(frame_number, colors_left)

        # created outline image cos no center circle outline
        self.paste(bg_img, CENTER_CIRCLE_OUTLINE_IMG_QUANTIZED, (
            int((DIMENSIONS[0] - CENTER_CIRCLE_RADIUS * 2) / 2), int((DIMENSIONS[1] - CENTER_CIRCLE_RADIUS * 2) /
                                                                     2)), CENTER_CIRCLE_OUTLINE_IMG)

        # add blink effect to triangle image on last frame
        if frame_number < NUM_SPIN_FRAMES or frame_number % 2 == 1:
            self.paste(bg_img, TRIANGLE_IMG_QUANTIZED, mask=TRIANGLE_IMG)

        # store stop frames to avoid recomputation
        if frame_number == NUM_SPIN_FRAMES:
            self.stop_frame_no_triangle = bg_img
        if frame_number == NUM_SPIN_FRAMES + 1:
            self.stop_frame_with_triangle = bg_img

        return bg_img


# for testing
# Spinner(123, ['ff', 'flavours'], True)
