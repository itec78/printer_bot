# Telegram Printer Bot

This Python script implements a Telegram bot that can print images and stickers sent by users. The bot supports resizing images, converting them to grayscale, and applying gamma correction before printing to ensure maximum quality.

Currently, you can set a command to print your sticker (by default we used brother_ql to print to a Brother printer). You can use any external program you want to print to other brands and models of printers.

## Requirements

* Python 3.6+
* telethon
* PIL (Python Imaging Library) library (Pillow)
* brother_ql

You can install the requirements by running this command:

`python3 -m pip install -r requirements.txt`

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

## Important Notes

1. Make sure to set proper permissions for the cache directory to ensure the bot can write to it.
2. The PRINT_COMMAND and PRINT_SUCCESS_COMMAND in the config.py file should be customized to match the print command on your system.
3. Ensure you have a functioning printer setup before running the bot. You will find the output from the command in the console!

## License

This project is licensed under the BEER-WARE License.

```/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <phk@FreeBSD.ORG> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp
 * ----------------------------------------------------------------------------
 */```

**This script is provided as-is, without any warranty or support. Use it at your own risk. The authors are not responsible for any misuse or damage caused by this script.**
