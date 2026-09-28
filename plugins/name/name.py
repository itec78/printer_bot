import os
from PIL import Image, ImageFont, ImageDraw

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

NAME = "name"
COMMANDS = ["name", "nome"]
REQUIRES_TEXT = True
REQUIRES_IMAGE = False


def run(msgtext, img):
	margin = 50
	size = 500  # Font size
	img = Image.open(os.path.join(PLUGIN_DIR, "Hello_my_name_is_sticker.png")).convert("RGBA")

	width, height = img.size
	while size > 20:
		font = ImageFont.truetype(os.path.join(PLUGIN_DIR, "DejaVuSans_NotoEmoji-Regular.ttf"), size)
		textwidth = font.getlength(msgtext)
		if textwidth <= width - (margin * 2):
			break
		else:
			size -= 5
	x = (width - textwidth) // 2

	ImageDraw.Draw(img).multiline_text((width / 2, height / 2 + 100), msgtext, (0, 0, 0), font=font, anchor="mm", align='center')
	return img
