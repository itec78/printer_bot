import os

import cowsay
from PIL import Image, ImageDraw, ImageFont

from config import MAX_ASPECT_RATIO

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(PLUGIN_DIR, "DejaVuSansMono.ttf")

NAME = "cowsay"
COMMANDS = ["cowsay", "cow"]
REQUIRES_TEXT = True
REQUIRES_IMAGE = False


def run(msgtext, img):
	margin = 50
	message = cowsay.get_output_string("cow", msgtext).rstrip("\n")

	canvas = Image.new(size=(100, 100), mode="RGB", color="white")
	size = 1
	while True:
		font = ImageFont.truetype(FONT_PATH, size)
		x, y, w, h = ImageDraw.Draw(canvas).multiline_textbbox((0, 0), message, font=font, spacing=0)
		if w > 2560 or h > 2560:
			break
		size += int(size * 0.2 + 1)

	nw = int(w - x + margin * 2)
	nh = int(h - y + margin * 2)
	nx = int(margin - x)
	ny = int(margin - y)

	if nw / nh > MAX_ASPECT_RATIO:
		nnh = int(nw / MAX_ASPECT_RATIO)
		ny += int((nnh - nh) / 2)
		nh = nnh

	canvas = Image.new(size=(nw, nh), mode="RGB", color="white")
	ImageDraw.Draw(canvas).multiline_text((nx, ny), message, font=font, fill="black", spacing=0)
	return canvas