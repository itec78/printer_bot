import os
from PIL import Image, ImageFont, ImageDraw

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

NAME = "asciiart2"
COMMANDS = ["aart2", "ascii2"]
REQUIRES_TEXT = False
REQUIRES_IMAGE = True

RAMP = "@%#*+=-:. "  # dense (dark) to sparse (light)
COLUMNS = 100


def _char_aspect(font_path, size=100):
	"""Width/height ratio of a single monospace character cell for our ramp charset."""
	font = ImageFont.truetype(font_path, size)
	draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))
	char_w = font.getlength(RAMP) / len(RAMP)
	_, y1, _, h1 = draw.multiline_textbbox((0, 0), RAMP, font=font, spacing=0)
	_, y2, _, h2 = draw.multiline_textbbox((0, 0), RAMP + "\n" + RAMP, font=font, spacing=0)
	line_h = (h2 - y2) - (h1 - y1)
	return char_w / line_h


def _to_ascii(img, columns, rows):
	img = img.convert("L")
	pixels = img.resize((columns, rows)).load()

	lines = []
	for y in range(rows):
		line = "".join(RAMP[min(len(RAMP) - 1, pixels[x, y] * len(RAMP) // 256)] for x in range(columns))
		lines.append(line)
	return "\n".join(lines)


def run(msgtext, img):
	margin = 50
	font_path = os.path.join(PLUGIN_DIR, "DejaVuSansMono.ttf")

	src_w, src_h = img.size
	char_aspect = _char_aspect(font_path)
	rows = max(1, round(COLUMNS * char_aspect * src_h / src_w))
	text = _to_ascii(img, COLUMNS, rows)

	canvas = Image.new(size=(100, 100), mode='RGB', color='white')
	size = 1
	while True:
		font = ImageFont.truetype(font_path, size)
		x, y, w, h = ImageDraw.Draw(canvas).multiline_textbbox((0, 0), text, font=font, spacing=0)
		if w > 2560 or h > 2560:
			break
		size += int(size * 0.2 + 1)

	# calc size with margin
	nw = int(w - x + (margin * 2))
	nh = int(h - y + (margin * 2))
	nx = int(margin - x)
	ny = int(margin - y)

	canvas = Image.new(size=(nw, nh), mode='RGB', color='white')
	ImageDraw.Draw(canvas).multiline_text((nx, ny), text, font=font, fill="black", spacing=0)
	return canvas
