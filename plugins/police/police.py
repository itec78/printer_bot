import os
from PIL import Image, ImageFont, ImageDraw, ImageOps
from config import MAX_ASPECT_RATIO

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

NAME = "police"
COMMANDS = ["police", "polizia"]
REQUIRES_TEXT = True
REQUIRES_IMAGE = False


def run(msgtext, img):
	margin = 50
	ratio = MAX_ASPECT_RATIO
	msgtext = msgtext.upper()

	alpha = Image.new('L', (100, 100), 0)
	size = 1
	while True:
		font = ImageFont.truetype(os.path.join(PLUGIN_DIR, "Roboto-Bold_NotoEmoji-Regular.ttf"), size)
		x, y, w, h = ImageDraw.Draw(alpha).multiline_textbbox((0, 0), msgtext, font=font, align='center')
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
	alpha = Image.new('L', (nw, nh), 0)
	ImageDraw.Draw(alpha).multiline_text((nx, ny), msgtext, font=font, fill="white", align='center')

	# crop and invert
	inv = ImageOps.invert(alpha.crop((0, int(nh / 2), nw, nh)))
	alpha.paste(inv, (0, int(nh / 2)))

	# apply alpha channel
	img = Image.new('RGBA', (nw, nh), (99, 151, 208))
	img.putalpha(alpha)

	# white background
	white_bg = Image.new("RGBA", img.size, "white")
	img = Image.alpha_composite(white_bg, img)
	return img
