import os
import tempfile
from PIL import Image, ImageOps
from ascii_magic import AsciiArt

NAME = "asciiart"
COMMANDS = ["aart", "ascii"]
REQUIRES_TEXT = False
REQUIRES_IMAGE = True

CONTRAST_FACTOR = 3  # pushes mid tones towards pure black/white
COLUMNS = 100


def run(msgtext, img):
	# Push mid tones towards pure black/white instead of just stretching the histogram
	source = img.convert("L").point(lambda p: int(255 / (1 + pow(2.718281828, -CONTRAST_FACTOR * (p / 255 - 0.5) * 6))))
	source = source.convert("RGB")

	# ascii_magic assumes a dark terminal background (bright pixel -> denser glyph),
	# so the source is inverted to get the right result with black ink on white paper
	source = ImageOps.invert(source)
	art = AsciiArt.from_pillow_image(source)

	fd, out_path = tempfile.mkstemp(suffix=".png")
	os.close(fd)
	try:
		art.to_image_file(out_path, columns=COLUMNS, monochrome=True, front="#000000", back="#FFFFFF")
		return Image.open(out_path).convert("RGB")
	finally:
		os.remove(out_path)
