import os
from PIL import Image, ImageFont, ImageDraw
from config import MAX_ASPECT_RATIO

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

NAME = "text"
COMMANDS = ["text", "testo"]
REQUIRES_TEXT = True
REQUIRES_IMAGE = False


def run(msgtext, img):
	margin = 50
	ratio = MAX_ASPECT_RATIO

	img = Image.new(size=(100, 100), mode='RGB', color='white')
	size = 1
	while True:
		font = ImageFont.truetype(os.path.join(PLUGIN_DIR, "DejaVuSans_NotoEmoji-Regular.ttf"), size)
		x, y, w, h = ImageDraw.Draw(img).multiline_textbbox((0, 0), msgtext, font=font, align='center')
		if w > 2560 or h > 2560:
			break
		size += int(size * 0.2 + 1)

	# calc size with margin
	nw = int(w - x + (margin * 2))
	nh = int(h - y + (margin * 2))
	nx = int(margin - x)
	ny = int(margin - y)

	# calc size with ratio
	if nw / nh > ratio:
		nnh = int(nw / ratio)
		ny = ny + int((nnh - nh) / 2)
		nh = nnh

	# draw text
	img = Image.new(size=(nw, nh), mode='RGB', color='white')
	ImageDraw.Draw(img).multiline_text((nx, ny), msgtext, font=font, fill="black", align='center')
	return img
