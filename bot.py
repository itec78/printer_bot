from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
import logging
from os import system
from time import time
from PIL import Image, ImageFont, ImageDraw, ImageOps
from config import *
import os
import json
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))
CACHE_DIR = os.path.join(SCRIPT_DIR,"cache")
PRINT_DIR = os.path.join(SCRIPT_DIR,"print")
EXTRA_DIR = os.path.join(SCRIPT_DIR,"extra")

print_log = {}

limitdict = {}
limit = {int(i.split("/")[1]): int(i.split("/")[0]) for i in AMOUNT_LIMIT.replace(" ","").split(",")}
limitfile = os.path.join(os.path.realpath(os.path.dirname(__file__)), "limit.json")

if os.path.isfile(limitfile):
	with open(limitfile, "r") as f: 
		limitdict = json.load(f)

async def debug_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await update.message.reply_text(f"Hello! Your id is `{update.message.from_user.id}` please add it to the ADMIN_ID to give youself privileges :)")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	msg = update.message
	await msg.reply_text(WELCOME_MSG)
	if PASSWORD:
		if (msg.from_user.id not in print_log):
			await msg.reply_text(UNLOCK_MSG)
			return

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	msg = update.message

	if PASSWORD:
		# This one triggers on a single message with the pin code written
		if msg.text:
			if msg.text.strip().lower() == PASSWORD.lower():
				if msg.from_user.id not in print_log:
					print_log[msg.from_user.id] = 0
					await msg.reply_text(UNLOCKED_MSG)
					return
		
		# Check for password
		if (msg.from_user.id not in print_log):
			await msg.reply_text(UNLOCK_MSG)
			return

	# Check if the file is valid
	fn = None
	imgcmd = None
	msgtext = ""

	if msg.photo:
		fid = msg.photo[-1].file_id
		fn = os.path.join(CACHE_DIR, f"{fid}.jpg")
	elif msg.sticker:
		fid = msg.sticker.file_id
		fn = os.path.join(CACHE_DIR, f"{fid}.webp")
	

	msgt = msg.text or msg.caption
	if msgt:
		msgl = msgt.strip().split(" ", 1)
		msgcmd = msgl[0].lower()
		msgtext = "" if len(msgl)<=1 else msgl[1] 

		if msgcmd in ["invert","inverti"]:
			imgcmd = "invert"
			if not fn:	
				await msg.reply_text("Invert: no image")
				return
		
		elif msgcmd in ["name","nome"]:
			imgcmd = "name"
			if msgtext == "":
				await msg.reply_text("Name: text missing")
				return


	if not fn and not imgcmd:
		await msg.reply_text(FORMAT_ERR_MSG)
		return
	


	# Check if the user is still in the cooldown period
	if msg.from_user.id != ADMIN_ID:
		l = list(sorted(limitdict.get(str(msg.from_user.id),[]),reverse=True))
		# print(l)
		for t in sorted([int(x) for x in limit.keys()], reverse=True):
			n = limit[t]
			# print(n,t)
			if len(l)>=n:
				dt = (datetime.now() - datetime.fromisoformat(l[n-1])).seconds - t
				# print(dt)
				if dt < 0:
					await msg.reply_text(RATELIMIT_MSG.format(time_left=str(timedelta(seconds=-dt))))
					return




	if fn:
		# Download the file unless it's in the cache!		
		if not os.path.isfile(fn):
			new_file = await context.bot.get_file(fid)
			await new_file.download_to_drive(fn)
		
		# Try opening the image, at least
		try:
			img = Image.open(fn)
		except:
			await msg.reply_text(FORMAT_ERR_MSG)
			return



	if imgcmd:

		if imgcmd == "invert":
			img = ImageOps.invert(img)

		elif imgcmd == "name":
			margin = 50
			size = 500 # Font size
			img = Image.open(os.path.join(EXTRA_DIR,"Hello_my_name_is_sticker.png")).convert("RGBA")

			width, height = img.size 
			while size > 20:
				font = ImageFont.load_default(size)
				textwidth = font.getlength(msgtext)
				if textwidth <= width-(margin*2):
					break
				else:
					size -= 5
			x = (width-textwidth)//2
			# print(size, width, textwidth, x)

			ImageDraw.Draw(img).multiline_text((width/2, height/2 + 100), msgtext, (0,0,0), font=font, anchor="mm", align='center')
			fn = os.path.join(CACHE_DIR, f"name_{' '.join(msgtext.splitlines())}.png".replace(" ","_"))
			img.save(fn)









	#Time to print!

	# Limit stickers ratio (so people don't print incredibly long stickers)
	if img.size[1]/img.size[0] > MAX_ASPECT_RATIO:
		await msg.reply_text(RATIO_ERR_MSG)
		return

	# Automatically rotate
	if AUTO_ROTATE:
		if img.size[0] > img.size[1] and not img.size[1]/img.size[0] > MAX_ASPECT_RATIO:
			img = img.rotate(90, expand=True)

	# Remove transparency
	if img.mode == 'RGBA':
		bg_img = Image.new(img.mode, img.size, BACKGROUND_COLOR)
		img = Image.alpha_composite(bg_img, img)

	# Resize the image
	img.thumbnail([WIDTH_PX, HEIGHT_PX], resample=Image.LANCZOS, reducing_gap=None)

	# Convert to grayscale and apply a gamma of 1.8
	img = img.convert('L')
	
	if GAMMA_CORRECTION != 1:
		img = Image.eval(img, lambda x: int(255*pow((x/255),(1/GAMMA_CORRECTION))))

	IMAGE_PATH = os.path.join(PRINT_DIR, os.path.basename(fn) + ".png")
	img.save(IMAGE_PATH, 'PNG')

	if msg.from_user.id != ADMIN_ID:
		await update.message.forward(ADMIN_ID)

	status_code = os.system(PRINT_COMMAND.format(IMAGE_PATH=IMAGE_PATH))
	if status_code == 0:
		print_log[msg.from_user.id] = time()
		
		#add
		if not str(msg.from_user.id) in limitdict:
			limitdict[str(msg.from_user.id)] = []
		limitdict[str(msg.from_user.id)].append(datetime.now().isoformat())
        #clean
		maxn = max([int(x) for x in limit.values()])
		limitdict[str(msg.from_user.id)] = limitdict[str(msg.from_user.id)][-maxn:]
		#save
		with open(limitfile, "w") as f: 
			json.dump(limitdict, f, indent=2)

		await msg.reply_text(PRINT_SUCCESS_MSG)
	else:
		await msg.reply_text(PRINT_FAIL_MSG)
		await application.bot.send_message(ADMIN_ID, f'Printer is not working. Process returned status code {status_code}')
	
	if PRINT_SUCCESS_COMMAND:
		os.system(PRINT_SUCCESS_COMMAND)

if __name__ == '__main__':
	os.makedirs(CACHE_DIR, exist_ok=True)
	os.makedirs(PRINT_DIR, exist_ok=True)

	application = Application.builder().token(BOT_TOKEN).build()
	application.add_handler(CommandHandler("start", welcome))
	application.add_handler(CommandHandler("id", debug_id))
	application.add_handler(MessageHandler(filters.ALL, handler))
	application.run_polling()
