import os
from PIL import Image, ImageFont, ImageDraw

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

NAME = "name"
COMMANDS = ["name", "nome"]
REQUIRES_TEXT = True
REQUIRES_IMAGE = False

# White rectangle in Hello_my_name_is_sticker.png (x, y, width, height)
BOX = (0, 276, 1024 - 0, 673 - 276)


def run(msgtext, img):
	margin = 50
	size = 500  # Font size
	img = Image.open(os.path.join(PLUGIN_DIR, "Hello_my_name_is_sticker.png")).convert("RGBA")

	bx, by, bw, bh = BOX

	size = 1
	while True:
		font = ImageFont.truetype(os.path.join(PLUGIN_DIR, "DejaVuSans_NotoEmoji-Regular.ttf"), size)
		x, y, w, h = ImageDraw.Draw(img).multiline_textbbox((0, 0), msgtext, font=font, align='center')
		if w > bw or h > bh:
			break
		size += int(size * 0.2 + 1)

	# calc size with margin
	nw = int(w - x + (margin * 2))
	nh = int(h - y + (margin * 2))
	nx = int(margin - x)
	ny = int(margin - y)

	# draw text
	imgtext = Image.new(size=(nw, nh), mode='RGB', color='white')
	ImageDraw.Draw(imgtext).multiline_text((nx, ny), msgtext, font=font, fill="black", align='center')

	imgtext.thumbnail((bw, bh))
	paste_x = bx + (bw - imgtext.width) // 2
	paste_y = by + (bh - imgtext.height) // 2
	img.paste(imgtext, (paste_x, paste_y))
	return img
