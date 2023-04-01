import math
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

DIMENSIONS = (500, 500)
CENTER = (250, 250)
RADIUS = 200
NUM_SPIN_FRAMES = 100
NUM_BLINK_FRAMES = 20
NUM_TOTAL_FRAMES = NUM_SPIN_FRAMES + NUM_BLINK_FRAMES
DURATIONS = [1000, 300, 200, 130, 80, 60, 40, 30, 25, 20] \
            + [20 for _ in range(NUM_SPIN_FRAMES - 20)] + [20, 25, 30, 40, 60, 80, 130, 200, 300, 1000] \
            + [100 for _ in range(NUM_BLINK_FRAMES)]  # Fastest 20
MASK_IMG = Image.open('mask.png')
SPINNER_CENTER_IMG = Image.open('spinner_center.png')
TRIANGLE_IMG = Image.open('triangle.png')


class SpinnerGifMaker:

    def __init__(self, options):
        random.shuffle(options)
        self.options = options
        colors = []
        for _ in enumerate(options):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            a = 128
            color = (r, g, b, a)
            colors.append(color)
        self.colors = colors
        start_angles = [-2, -5, -10, -15, -20, -30, -40, -60, -80, -100]
        for i in range(len(start_angles)):
            start_angles[i] = i * start_angles[i]
        end_angles = [-100, -80, -60, -40, -30, -20, -15, -10, -5, -2]
        for i in range(len(end_angles)):
            end_angles[i] = (len(end_angles) - i) * -end_angles[i] - 13000
        angles = start_angles + [i * -150 - 1000 for i in
                                 range(NUM_SPIN_FRAMES - 20)] + end_angles
        random_offset = random.randint(0, 359)
        self.angles = [i - random_offset for i in angles]

        frame_list = []
        for i in range(NUM_TOTAL_FRAMES):
            frame = self.getSpinnerFrame(i)
            frame_list.append(frame)
        frame_list[0].save('spinner.gif', format='GIF', append_images=frame_list[1:202], save_all=True,
                           duration=DURATIONS, disposal=2, loop=0)

    def getSpinnerFrame(self, frame_number):

        spinner_img = Image.new('RGB', DIMENSIONS, color=(255, 255, 255))
        spinner_draw = ImageDraw.Draw(spinner_img, 'RGBA')
        num_sections = len(self.options)
        for i, option in enumerate(self.options):
            start_angle = i * (360 / num_sections)
            end_angle = (i + 1) * (360 / num_sections)
            color = self.colors[i]
            spinner_draw.pieslice(xy=((CENTER[0] - RADIUS, CENTER[1] - RADIUS), (CENTER[0] + RADIUS, CENTER[1] +
                                                                                 RADIUS)),
                                  start=start_angle,
                                  end=end_angle, fill=color, outline='black')

            font = ImageFont.truetype("arial.ttf", 30)
            _, _, text_width, text_height = spinner_draw.textbbox((0, 0), option, font=font, anchor="lt")
            section_center_angle = (start_angle + end_angle) / 2
            section_center_x = CENTER[0] + RADIUS * 0.6 * math.cos(section_center_angle * math.pi / 180)
            section_center_y = CENTER[1] + RADIUS * 0.6 * math.sin(section_center_angle * math.pi / 180)
            text_angle = 180 - section_center_angle
            # print(i, option, text_angle, text_width, text_height)
            text_img = Image.new('RGBA', (text_width, text_height), color=(255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_draw.text((0, 0), option, fill=(0, 0, 0), font=font, anchor="lt")
            text_img = text_img.rotate(text_angle, expand=True)
            text_width, text_height = text_img.size
            text_center_x = section_center_x - text_width / 2
            text_center_y = section_center_y - text_height / 2
            spinner_img.paste(text_img, (int(text_center_x), int(text_center_y)), text_img)

        spinner_img.putalpha(MASK_IMG)
        # Add blink effect to triangle image on last frame
        if frame_number < NUM_SPIN_FRAMES:
            spinner_img = spinner_img.rotate(self.angles[frame_number], center=CENTER)
        else:
            spinner_img = spinner_img.rotate(self.angles[-1], center=CENTER)
        if frame_number < NUM_SPIN_FRAMES or frame_number % 2 == 1:
            spinner_img.paste(TRIANGLE_IMG, mask=TRIANGLE_IMG)
        spinner_img.paste(SPINNER_CENTER_IMG, mask=SPINNER_CENTER_IMG)
        return spinner_img

# SpinnerGifMaker(["hi", "play", "sleep", "run", "dance", "eat", "fly", "study"])
