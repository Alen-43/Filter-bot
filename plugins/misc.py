import os
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
from info import PICS
from info import IMDB_TEMPLATE
from utils import extract_user, get_file_id, get_poster, last_online
import time
import random
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == "private":
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(
            f"<b>➪ First Name:</b> {first}\n<b>➪ Last Name:</b> {last}\n<b>➪ Username:</b> {username}\n<b>➪ Telegram ID:</b> <code>{user_id}</code>\n<b>➪ Data Centre:</b> <code>{dc_id}</code>",
            quote=True
        )

    elif chat_type in ["group", "supergroup"]:
        _id = ""
        _id += (
            "<b>➛ Chat ID</b>: "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "<b>➛ User ID</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
                "<b>➛ Replied User ID</b>: "
                f"<code>{message.reply_to_message.from_user.id if message.reply_to_message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += (
                "<b>➛ User ID</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(
            _id,
            quote=True
        )

@Client.on_message(filters.command("about"))
async def aboutme(client, message):
        buttons= [[
            InlineKeyboardButton('➡️ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ⬅️', url='https://t.me/space_4_movies')
            ],[
            InlineKeyboardButton('ʙᴀᴄᴋ↩️', callback_data='start'),
            InlineKeyboardButton('❌️ᴄʟᴏsᴇ❌️', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.ABOUT_TXT.format(message.from_user.mention),
            reply_markup=reply_markup,
        )

@Client.on_message(filters.command(["info"]))
async def who_is(client, message):
    # https://github.com/SpEcHiDe/PyroGramBot/blob/master/pyrobot/plugins/admemes/whois.py#L19
    status_message = await message.reply_text(
        "`sᴇᴀʀᴄʜɪɴɢ ᴜsᴇʀ...`"
    )
    await status_message.edit(
        "`𝙰𝙲𝙲𝙴𝚂𝚂𝙸𝙽𝙶 𝙸𝙽𝙵𝙾𝚁𝙼𝙰𝚃𝙸𝙾𝙽...`"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        return await status_message.edit("no valid user_id / message specified")
    message_out_str = ""
    message_out_str += f"<b>➾ First Name:</b> {from_user.first_name}\n"
    last_name = from_user.last_name or "<b>None</b>"
    message_out_str += f"<b>➾ Last Name:</b> {last_name}\n"
    message_out_str += f"<b>➾ Telegram ID:</b> <code>{from_user.id}</code>\n"
    username = from_user.username or "<b>None</b>"
    dc_id = from_user.dc_id or "[User Doesnt Have A Valid DP]"
    message_out_str += f"<b>➾ Data Centre:</b> <code>{dc_id}</code>\n"
    message_out_str += f"<b>➾ User Name:</b> @{username}\n"
    message_out_str += f"<b>➾ User 𝖫𝗂𝗇𝗄:</b> <a href='tg://user?id={from_user.id}'><b>Click Here</b></a>\n"
    if message.chat.type in (("supergroup", "channel")):
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += (
                "<b>➾ Joined this Chat on:</b> <code>"
                f"{joined_date}"
                "</code>\n"
            )
        except UserNotParticipant:
            pass
    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )
        buttons = [[
            InlineKeyboardButton('❌️ᴄʟᴏsᴇ❌️', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            reply_markup=reply_markup,
            caption=message_out_str,
            disable_notification=True
        )
        os.remove(local_user_photo)
    else:
        buttons = [[
            InlineKeyboardButton('❌️ᴄʟᴏsᴇ❌️', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=message_out_str,
            reply_markup=reply_markup,
            quote=True,
            disable_notification=True
        )
    await status_message.delete()

@Client.on_message(filters.command("help"))
async def help(client, message):
        buttons = [[
            InlineKeyboardButton('ᴍᴀɴᴜᴇʟ ғɪʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('ᴀᴜᴛᴏ ғɪʟᴛᴇʀ', callback_data='autofilter'),   
            ],[
            InlineKeyboardButton('ᴄᴏɴɴᴇᴄᴛɪᴏɴs', callback_data='coct')
            ],[
            InlineKeyboardButton('sᴏɴɢ', callback_data='songs'),
            InlineKeyboardButton("ᴠɪᴅᴇᴏ", callback_data='video')
            ],[
            InlineKeyboardButton('ᴇxᴛʀᴀ', callback_data='extra')
            ],[
            InlineKeyboardButton('ᴘɪɴ', callback_data='pin'), 
            InlineKeyboardButton('ᴘᴀsᴛᴇ', callback_data='pastes'),
            InlineKeyboardButton("ɪᴍᴀɢᴇ", callback_data='image')
            ],[
            InlineKeyboardButton('ᴄᴀʀʙᴏɴ', callback_data='fun'), 
            InlineKeyboardButton('ғᴏɴᴅ', callback_data='son'),
            InlineKeyboardButton('ᴛᴛs', callback_data='ttss')
            ],[
            InlineKeyboardButton('ᴘᴜʀɢᴇ', callback_data='purges'),
            InlineKeyboardButton('ᴘɪɴɢ', callback_data='pings'),
            InlineKeyboardButton('ᴛᴇʟᴇɢʀᴀᴘʜ', callback_data='tele')
            ],[
            InlineKeyboardButton('ᴡʜᴏɪs', callback_data='whois'),
            InlineKeyboardButton('ᴍᴜᴛᴇ', callback_data='restric'),
            InlineKeyboardButton('ᴋɪᴄᴋ', callback_data='zombies')
            ],[
            InlineKeyboardButton('ʀᴇᴘᴏʀᴛ', callback_data='report'),
            InlineKeyboardButton('ʏᴛ-ᴛʜᴜᴍʙ', callback_data='ytthumb'),
            InlineKeyboardButton('sᴛɪᴄᴋᴇʀ-ɪᴅ', callback_data='sticker')
            ],[
            InlineKeyboardButton('ᴄᴏᴠɪᴅ', callback_data='corona'),
            InlineKeyboardButton('ᴀᴜᴅɪᴏ-ʙᴏᴏᴋ', callback_data='abook'),
            InlineKeyboardButton('ᴜʀʟ-sʜᴏʀᴛ', callback_data='urlshort')
            ],[
            InlineKeyboardButton('ɢ-ᴛʀᴀɴs', callback_data='gtrans'),
            InlineKeyboardButton('ғɪʟᴇ-sᴛᴏʀᴇ', callback_data='newdata'),
            InlineKeyboardButton('sᴛᴀᴛᴜs', callback_data='stats')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.HELP_TXT.format(message.from_user.mention),
            reply_markup=reply_markup
        )


@Client.on_message(filters.command(["imdb", 'search']))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('Searching ImDB')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("No results Found")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('Here is what i found on IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Give me a movie / series Name')

@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot: Client, query: CallbackQuery):
    i, movie = query.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{imdb.get('title')}",
                    url=imdb['url'],
                )
            ]
        ]
    if imdb:
        caption = IMDB_TEMPLATE.format(
            group = message.chat.title,
            requested = message.from_user.mention,        
            query = imdb['title'],
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url']
        )
    else:
        caption = "No Results"
    if imdb.get('poster'):
        try:
            await query.message.reply_photo(photo=imdb['poster'], caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await query.message.reply_photo(photo=imdb['poster'], caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            await query.message.reply(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
        await query.message.delete()
    else:
        await query.message.edit(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
    await query.answer()
        

        
