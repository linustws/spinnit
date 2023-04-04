import math
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from components_creator import create_images

DIMENSIONS = (500, 500)
CENTER = (250, 250)
RADIUS = 225
DIAMETER = RADIUS * 2
CENTER_CIRCLE_RADIUS = 100
NUM_SPIN_FRAMES = 100
NUM_BLINK_FRAMES = 20
NUM_TOTAL_FRAMES = NUM_SPIN_FRAMES + NUM_BLINK_FRAMES
DURATIONS = [1000, 300, 200, 130, 80, 60, 40, 30, 25, 20] \
            + [20 for _ in range(NUM_SPIN_FRAMES - 20)] + [20, 25, 30, 40, 60, 80, 130, 200, 300, 1000] \
            + [100 for _ in range(NUM_BLINK_FRAMES)]  # Fastest 20
try:
    MASK_IMG = Image.open('mask.png')
    CENTER_CIRCLE_MASK_IMG = Image.open('center_circle_mask.png')
    CENTER_CIRCLE_OUTLINE_IMG = Image.open('center_circle_outline.png')
    TRIANGLE_IMG = Image.open('triangle.png')
except FileNotFoundError as e:
    create_images(DIMENSIONS, CENTER, RADIUS, CENTER_CIRCLE_RADIUS)
    MASK_IMG = Image.open('mask.png')
    CENTER_CIRCLE_MASK_IMG = Image.open('center_circle_mask.png')
    CENTER_CIRCLE_OUTLINE_IMG = Image.open('center_circle_outline.png')
    TRIANGLE_IMG = Image.open('triangle.png')
PASTEL_COLORS = [(220, 214, 255), (214, 240, 255), (222, 255, 239), (255, 250, 240), (255, 237, 237),
                 (255, 222, 222), (247, 246, 207), (182, 216, 242), (244, 207, 223), (87, 132, 186),
                 (154, 200, 235), (204, 212, 191), (231, 203, 169), (238, 186, 178), (245, 243, 231),
                 (245, 226, 228), (245, 191, 210), (229, 219, 156), (208, 188, 172), (190, 180, 197),
                 (230, 165, 126), (33, 139, 130), (154, 217, 219), (229, 219, 217), (152, 212, 187),
                 (235, 150, 170), (198, 201, 208), (229, 179, 187), (196, 116, 130), (249, 150, 139),
                 (118, 205, 205), (123, 146, 170), (228, 206, 224), (161, 93, 152), (220, 130, 143),
                 (247, 206, 118), (140, 115, 134), (156, 147, 89), (165, 114, 131), (232, 213, 149)]


class SpinnerGifMaker:

    def __init__(self, options):
        random.shuffle(options)
        self.options = options
        # must be 450 x 450
        self.center_circle_img = Image.open("images/cat.png")
        self.colors = random.sample(PASTEL_COLORS, len(options))
        start_angles = [-2, -5, -10, -15, -20, -30, -40, -60, -80, -100]
        for i in range(len(start_angles)):
            start_angles[i] = i * start_angles[i]
        end_angles = [-100, -80, -60, -40, -30, -20, -15, -10, -5, -2]
        for i in range(len(end_angles)):
            end_angles[i] = (len(end_angles) - i) * -end_angles[i] - 13000
        angles = start_angles + [i * -150 - 1000 for i in
                                 range(NUM_SPIN_FRAMES - 20)] + end_angles
        start_offset = random.randint(0, 359)
        end_offset = random.randint(0, 359)
        first_half = angles[:50]
        second_half = angles[50:]
        first_half = [angle - start_offset for angle in first_half]
        second_half = [angle - end_offset for angle in second_half]
        self.angles = first_half + second_half
        # print(self.angles[49] - self.angles[48], self.angles[50] - self.angles[49], self.angles[51] - self.angles[50])

        frame_list = []
        for i in range(NUM_TOTAL_FRAMES):
            frame = self.getSpinnerFrame(i)
            frame_list.append(frame)
        frame_list[0].save('spinner.gif', format='GIF', append_images=frame_list[1:], save_all=True,
                           duration=DURATIONS, disposal=2, loop=0)

    def getSpinnerFrame(self, frame_number):

        spinner_img = Image.new('RGB', DIMENSIONS, color=(0, 0, 0))
        # Add color pie slices
        spinner_draw = ImageDraw.Draw(spinner_img, 'RGBA')
        num_sections = len(self.options)
        for i, option in enumerate(self.options):
            start_angle = i * (360 / num_sections)
            end_angle = (i + 1) * (360 / num_sections)
            color = self.colors[i]
            opacity = (255,)
            # if frame_number < 20:
            #     opacity = opacity + (255,)
            # elif frame_number >= 90:
            #     opacity = opacity + (0,)
            # else:
            #     opacity_value = int((NUM_TOTAL_FRAMES - frame_number) / NUM_TOTAL_FRAMES * 255)
            #     opacity = opacity + (opacity_value,)
            spinner_draw.pieslice(xy=((CENTER[0] - RADIUS, CENTER[1] - RADIUS), (CENTER[0] + RADIUS, CENTER[1] +
                                                                                 RADIUS)),
                                  start=start_angle,
                                  end=end_angle, fill=color + opacity, outline='black')

            # Add text options
            font = ImageFont.truetype("arial.ttf", 30)
            _, _, text_width, text_height = spinner_draw.textbbox((0, 0), option, font=font, anchor="lt")
            section_center_angle = (start_angle + end_angle) / 2
            section_center_x = CENTER[0] + (RADIUS + CENTER_CIRCLE_RADIUS) * 0.5 * math.cos(section_center_angle *
                                                                                            math.pi / 180)
            section_center_y = CENTER[1] + (RADIUS + CENTER_CIRCLE_RADIUS) * 0.5 * math.sin(section_center_angle *
                                                                                            math.pi / 180)
            text_angle = 180 - section_center_angle
            text_img = Image.new('RGBA', (text_width, text_height), color=(0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_draw.text((0, 0), option, fill=(0, 0, 0), font=font, anchor="lt")
            text_img = text_img.rotate(text_angle, expand=True)
            text_width, text_height = text_img.size
            text_center_x = section_center_x - text_width / 2
            text_center_y = section_center_y - text_height / 2
            spinner_img.paste(text_img, (int(text_center_x), int(text_center_y)), text_img)

        center_circle_img = self.center_circle_img.copy()
        center_circle_img.putalpha(CENTER_CIRCLE_MASK_IMG)

        spinner_img.paste(center_circle_img, (
            int((DIMENSIONS[0] - CENTER_CIRCLE_RADIUS * 2) / 2), int((DIMENSIONS[1] - CENTER_CIRCLE_RADIUS * 2) /
                                                                     2)), center_circle_img)

        spinner_img.paste(CENTER_CIRCLE_OUTLINE_IMG, (
            int((DIMENSIONS[0] - CENTER_CIRCLE_RADIUS * 2) / 2), int((DIMENSIONS[1] - CENTER_CIRCLE_RADIUS * 2) /
                                                                     2)), CENTER_CIRCLE_OUTLINE_IMG)

        spinner_img.putalpha(MASK_IMG)
        # Add blink effect to triangle image on last frame
        if frame_number < NUM_SPIN_FRAMES:
            spinner_img = spinner_img.rotate(self.angles[frame_number], center=CENTER)
        else:
            spinner_img = spinner_img.rotate(self.angles[-1], center=CENTER)
        if frame_number < NUM_SPIN_FRAMES or frame_number % 2 == 1:
            spinner_img.paste(TRIANGLE_IMG, mask=TRIANGLE_IMG)

        return spinner_img


SpinnerGifMaker(["hi", "play", "sleep", "run", "dance", "eat", "fly", "study"])
