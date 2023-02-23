#!/usr/bin/env python
from collections import deque
import os
from PIL import Image
import requests
import sys
import telepot
import time

handled_updates = []

try:
    BOT_TOKEN = "5998737564:AAH19LlVDCRzXYv0T6UDgEDL36wwmwUxNGc"
except KeyError:
    BOT_TOKEN = sys.argv[1]

endpoint = f'https://api.telegram.org/bot{BOT_TOKEN}'
file_endpoint = f'https://api.telegram.org/file/bot{BOT_TOKEN}'

def inc_uses():
    try:
        with open("uses.txt") as f:
            uses = int(f.read().split("\n")[0].strip())
    except:
        uses = 0
    
    with open("uses.txt", "w") as f:
        f.write(str(uses+1))

def resize_image(path):
    img = Image.open(path)
    ratio = 512/max(img.size)
    new_size = (int(img.size[0]*ratio), int(img.size[1]*ratio))
    img = img.resize(new_size, Image.ANTIALIAS)
    img.save(path + ".png", "png")
    return path + ".png"

def chat_handler(msg):
    msg_type, chat_type, chat_id = telepot.glance(msg)

    if "reply_to_message" in msg and "/crop" in msg["text"]:
        msg = msg["reply_to_message"]
        msg_type, chat_type, chat_id = telepot.glance(msg)
    elif not msg_type in ["document", "photo"]:
        return


    # Handle compressed/uncompressed images
    if msg_type == "document":
        if msg["document"]["mime_type"] in ["image/png", "image/jpeg"]:
            file_id = msg["document"]["file_id"]
        else:
            return
    elif msg_type == "photo":
        file_id = msg["photo"][-1]["file_id"]
    else:
        return

    file_path = "downloads/" + bot.getFile(file_id)["file_path"].split("/")[1]

    # Download file
    bot.download_file(file_id, file_path)

    # Resize and send file
    new_file_path = resize_image(file_path)
    with open(new_file_path, "rb") as f:
        bot.sendDocument(chat_id, f)
    
    inc_uses()

    # Clean up working directory
    os.remove(file_path)
    os.remove(new_file_path)

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Instantiate bot
    bot = telepot.Bot(BOT_TOKEN)

    # New message listener
    bot.message_loop({'chat' : chat_handler},
                      run_forever="Bot Running...")

