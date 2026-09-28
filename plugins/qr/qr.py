import qrcode

NAME = "qr"
COMMANDS = ["qr", "qrcode"]
REQUIRES_TEXT = True
REQUIRES_IMAGE = False


def run(msgtext, img):
	qr = qrcode.QRCode(
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=50,
		border=2
	)
	qr.add_data(msgtext)
	qr.make()
	return qr.make_image()
