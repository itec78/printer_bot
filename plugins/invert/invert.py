from PIL import ImageOps

NAME = "invert"
COMMANDS = ["invert", "inverti"]
REQUIRES_TEXT = False
REQUIRES_IMAGE = True


def run(msgtext, img):
	return ImageOps.invert(img)
