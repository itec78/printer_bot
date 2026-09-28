# Telegram Sticker Printer Bot

This is a fork of [foxo/printer_bot](https://git.foxo.me/foxo/printer_bot) with a few improvements:

* Uses `python-telegram-bot` instead of `telethon`
* Automatic image rotation (`AUTO_ROTATE`) to better fit the printer's aspect ratio
* Rate limiting on the number of prints per user (`AMOUNT_LIMIT`)
* Image-generating and editing commands: `invert`, `name`, `text`, `qr`, `police`, `ascii`, `ascii2`, `cowsay`
* Privacy options: optionally delete files after printing (`KEEP_FILES`) and forward prints to the admin (`ADMIN_FORWARD`)
* Uses a maintained fork of `brother_ql` ([matmair/brother_ql-inventree](https://github.com/matmair/brother_ql-inventree))
* Pluggable commands: image-generating commands live under `plugins/` and are loaded automatically (see [Plugins](#plugins))

This Python script implements a Telegram bot that can print images and stickers sent by users. The bot supports resizing images, converting them to grayscale, and applying gamma correction before printing to ensure maximum quality.

Currently, you can set any command to print your sticker (by default brother_ql is used to print). You can use any external program you want to print to other brands and models of printers.

## Tested printers

* Brother QL-700 / QL-800 / QL-500 (brother_ql)

## Recommended label rolls

It is important to use "continuous" rolls when using Brother printers, aka ones which are not precut and have an endless roll of thermal paper. Although you can also use smaller sizes, 62mm wide rolls are suggested.

There are a variety of label rolls you can buy:
* DK-44205, DK-22205: paper, black on white
* DK-44605: paper, black on yellow
* DK-22606: plastic film, black on yellow
* DK-22113: plastic film, black on transparent

Be careful of models that don't feature glue! Make sure whatever you buy is a label and not just a roll :)

## Requirements

* Python 3.6+
* python-telegram-bot
* PIL (Python Imaging Library) library (Pillow)
* brother_ql

You can install the requirements by running this command:

```bash
python3 -m pip install -r requirements.txt
for requirements in plugins/*/requirements.txt; do
  python3 -m pip install -r "$requirements"
done
```

This also installs the dependencies of every plugin under `plugins/` (see [Plugins](#plugins) below).

If this is the first time running the script and your printer uses the `lp` protocol, remember to add your user to the `lp` group using the following command:

`sudo usermod -a -G lp ${USER}`

## Configuration

Before running the script, you need to set up the configuration parameters. You can use "config.example.py" as a guide (rename it to config.py). The following parameters must be defined:

* API_ID: Your Telegram API ID. You can obtain it by creating a Telegram application
* API_HASH: Your Telegram API hash. You can obtain it from the same page where you got the API ID.
* BOT_TOKEN: The token for your Telegram bot. You can create a new bot and obtain the token by following the instructions here.
* ADMIN_ID: Your user id. This is the user that will receive administrative rights and error reports.
* PRINT_COMMAND: Adjust with your printer model and path.

## Usage

After setting up the configuration file, you can just run the bot by using the command

`python bot.py`

Once the bot is running, it will respond to specific commands:

* `/id`: Returns your Telegram user ID, which you need to add to the ADMIN_ID list in the config.py file to grant yourself privileges.
* `/start`: Displays a welcome message and requests a password if set in the config.py file.
    When the user sends the correct password in a private message, the printer functionality will be unlocked for that user.

## Features

* Printer password (pin code) protection
* Cooldown period for users
* Caching of images and stickers
* Resizing images to the correct printer resolution for maximum crispness
* Conversion to greyscale with gamma adjustment (improves images a lot!)
* Ratio limit to prevent excessively long stickers from being printed

## Plugins

Commands that generate or transform an image (`name`, `text`, `qr`, `police`, `invert`, ...) are implemented as plugins under `plugins/`. Each plugin lives in its own folder together with any asset it needs (fonts, images, its own `requirements.txt`, etc.):

```
plugins/
  cowsay/
    cowsay.py
    DejaVuSansMono.ttf
    requirements.txt
  qr/
    qr.py
    requirements.txt
  name/
    name.py
    Hello_my_name_is_sticker.png
    DejaVuSans_NotoEmoji-Regular.ttf
```

Available plugin commands include:

* `invert`: invert an image.
* `name`: add a name sticker to an image.
* `text`: render text as an image.
* `qr`: generate a QR code from text.
* `police`: apply the police effect to an image.
* `ascii` / `aart`: convert an image to ASCII art.
* `ascii2` / `aart2`: convert an image to monospace ASCII art.
* `cowsay` / `cow`: render text using the Python `cowsay` library.

At startup, `bot.py` loads every folder in `plugins/` automatically, so adding a new command doesn't require touching any core code. To add a new plugin:

1. Create a new folder under `plugins/`, e.g. `plugins/mycommand/`.
2. Add a Python file in it (matching the folder name if the folder contains more than one `.py` file) that defines:
   * `NAME`: the plugin's display name, used for cache filenames and error messages.
   * `COMMANDS`: a list of command aliases that trigger the plugin (e.g. `["qr", "qrcode"]`).
   * `REQUIRES_TEXT`: whether the command needs text after it (e.g. `/qr some text`).
   * `REQUIRES_IMAGE`: whether the command needs an image/sticker already attached to the message.
   * `run(msgtext, img)`: returns the resulting `PIL.Image`.
3. Put any asset the plugin needs (fonts, images) in the same folder, and resolve them relative to the file, e.g. `os.path.dirname(os.path.abspath(__file__))`.
4. If the plugin needs extra Python packages, add them to a `requirements.txt` in the plugin folder.

## Important Notes

1. Make sure to set proper permissions for the cache directory to ensure the bot can write to it.
2. The PRINT_COMMAND and PRINT_SUCCESS_COMMAND in the config.py file should be customized to match the print command on your system.
3. Ensure you have a functioning printer setup before running the bot. You will find the output from the command in the console!

## License

This project is licensed under the BEER-WARE License.

```

/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * foxo (@git.foxo.me) wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.  ~ Foxo
 * ----------------------------------------------------------------------------
 */

```


**This script is provided as-is, without any warranty or support. Use it at your own risk. The authors are not responsible for any misuse or damage caused by this script.**
