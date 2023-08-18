from telethon import TelegramClient
import logging, asyncio
from telethon.tl.types import MessageMediaDocument, DocumentAttributeSticker, DocumentAttributeAnimated, MessageMediaPhoto
from telethon import events
from telethon.tl.custom import Button
from os.path import isfile, join
from os import system
from time import time
from PIL import Image
from config import *
from os import makedirs

logging.basicConfig(level=logging.INFO)

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
client.flood_sleep_threshold = 120

print_log = {}

@client.on(events.NewMessage(pattern='^/id'))
async def debug_id(ev):
	await ev.respond(f"Hello! Your id is `{ev.peer_id.user_id}` please add it to the ADMIN_ID to give youself privileges :)")

@client.on(events.NewMessage(pattern='^/start'))
async def welcome(ev):
	await ev.respond(WELCOME_MSG)
	if (ev.peer_id.user_id not in print_log) and PASSWORD:
		await ev.respond(UNLOCK_MSG)

# This one triggers on a single message with the pin code written
@client.on(events.NewMessage(pattern=PASSWORD, func=lambda e: e.is_private))
async def unlock_printer(ev):
	if ev.peer_id.user_id not in print_log:
		print_log[ev.peer_id.user_id] = 0
		if PASSWORD:
			await ev.respond(UNLOCKED_MSG)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.message.media))
async def handler(ev):

	msg = ev.message
	if ev.peer_id.user_id not in print_log:
		await ev.respond(UNLOCK_MSG)

	# Check if the file is valid
	if msg.photo:
		fn = join(CACHE_DIR, f"{msg.photo.id}.jpg")
	elif msg.sticker:
		fn = join(CACHE_DIR, f"{msg.sticker.id}.webp")
		for att in msg.sticker.attributes:
			if isinstance(att, DocumentAttributeAnimated):
				fn = None
				break
	else:
		fn = None
		
	if not fn:
		await ev.respond(FORMAT_ERR_MSG)
		return
	
	# Check if the user is still in the cooldown period
	time_left = int((print_log[ev.peer_id.user_id] + BASE_COOLDOWN) - time())
	if time_left > 0:
		await ev.respond(RATELIMIT_MSG.format(time_left=time_left))
		return

	# Download the file unless it's in the cache!		
	if not isfile(fn):
		await client.download_media(msg, file=fn)
	
	# Try opening the image, at least
	try:
		img = Image.open(fn)
	except:
		await ev.respond(FORMAT_ERR_MSG)
		return
	
	# Limit stickers ratio (so people don't print incredibly long stickers)
	if img.size[1]/img.size[0] > MAX_ASPECT_RATIO:
		await ev.respond(RATIO_ERR_MSG)
		return

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

	img.save(IMAGE_PATH, 'PNG')

	await client.forward_messages(ADMIN_ID, ev.message)

	status_code = system(PRINT_COMMAND)
	if status_code == 0:
		print_log[ev.peer_id.user_id] = time()
		await ev.respond(PRINT_SUCCESS_MSG)
	else:
		await ev.respond(PRINT_FAIL_MSG)
		await client.send_message(ADMIN_ID, f'Printer is not working. Process returned status code {status_code}')
	
	if PRINT_SUCCESS_COMMAND:
		system(PRINT_SUCCESS_COMMAND)

if __name__ == '__main__':
	makedirs(CACHE_DIR, exist_ok=True)
	client.run_until_disconnected()
