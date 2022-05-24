import os
import time
import ytthumb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(["ytthumb", 'dlthumb']))
async def send_thumbnail(bot, update):
    message = await update.reply_text(
        text="`ɢᴇɴᴇʀᴀᴛɪɴɢ ᴛʜᴜᴍʙɴᴀɪʟ...`",
        disable_web_page_preview=True,
        quote=True
    )
    try:
        if " | " in update.text:
            video = update.text.split(" | ", -1)[0]
            quality = update.text.split(" | ", -1)[1]
        else:
            video = update.text
            quality = "sd"
        thumbnail = ytthumb.thumbnail(
            video=video,
            quality=quality
        )
        await update.reply_photo(
            photo=thumbnail,
            quote=True
        )
        await message.delete()
    except Exception as error:
        await message.edit_text(
            text="**Please Use** /ytthumb (youtube link)\n\n**Example:** `/ytthumb https://youtu.be/examplelink`",
            disable_web_page_preview=True
        )
