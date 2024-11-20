
# To get an API_ID and API_HASH, you need to sign up to be a Telegram Dev.
# Do it here: https://core.telegram.org/api/obtaining_api_id
API_ID = 11111
API_HASH = '5d41402abc4b2a76b9719d911017c592'

# Get a bot token from Telegram by creating a bot with @BotFather
BOT_TOKEN = '1222222222:b2YgZXdvaWZld29maHdlb2lmaA'

WELCOME_MSG = 'Hello!\nWelcome to **Foxo\'s label printer**! Send me any sticker or other media to print it!'
UNLOCK_MSG = 'The printer is currently locked for you. Please enter the password!'
PRINT_FAIL_MSG = 'I wasn\'t able to print your sticker.'
RATIO_ERR_MSG = 'That image is too tall. It would waste a lot of paper. Please give me a shorter sticker.'
PRINT_SUCCESS_MSG = 'Your sticker has finished printing now! Enjoy it :3'
FORMAT_ERR_MSG = 'Cannot print this. Try with a (static) sticker or a picture!'
RATELIMIT_MSG = 'Woo calm down fam!\n\nSend the sticker again in {time_left} seconds!'
UNLOCKED_MSG = 'Printer has been unlocked. Have fun!'

# Limits to prevent abuse
PASSWORD = '12345' # Set to None if no password required
BASE_COOLDOWN = 10 # Seconds between stickers printing
MAX_ASPECT_RATIO = 1.5 # Maximum ratio between height/width of sticker
ADMIN_ID = 111111 # Find your own id with the /id command

# Remember to add your user to the "lp" group or this won't work!
PRINT_COMMAND = "brother_ql -m QL-700 -b linux_kernel -p file:///dev/usb/lp0 print -l 62 [IMAGE_PATH] -d"
PRINT_SUCCESS_COMMAND = None # "mpv --no-video success.wav" - this was used to play audio

# Resize and process settings
WIDTH_PX = 696
HEIGHT_PX = 9999 # This means "do not care about height"
GAMMA_CORRECTION = 1.8
BACKGROUND_COLOR = 'white'
