from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.enums import ChatAction
from config import youtube_next_fetch
from helper.ytdlfunc import extractYt, create_buttons
import wget
import os
from PIL import Image

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
user_time = {}

@Client.on_message(filters.regex(ytregex))
async def ytdl(client, message):
    userLastDownloadTime = user_time.get(message.chat.id)
    try:
        if userLastDownloadTime and userLastDownloadTime > datetime.now():
            wait_time = round((userLastDownloadTime - datetime.now()).total_seconds() / 60, 2)
            await message.reply_text(f"`انتظر {wait_time} دقيقة قبل الطلب القادم`")
            return
    except Exception:
        pass

    url = message.text.strip()
    await message.reply_chat_action(ChatAction.TYPING)
    try:
        title, thumbnail_url, formats = extractYt(url)
        now = datetime.now()
        user_time[message.chat.id] = now + timedelta(minutes=youtube_next_fetch)
    except Exception:
        await message.reply_text("`فشل في جلب بيانات اليوتيوب... 😔\nربما تم حظر اليوتيوب على الخادم\n#error`")
        return
    buttons = InlineKeyboardMarkup(list(create_buttons(formats)))
    sentm = await message.reply_text("جارٍ معالجة الرابط 🔎🔎🔎")
    try:
        img = wget.download(thumbnail_url)
        im = Image.open(img).convert("RGB")
        output_directory = os.path.join(os.getcwd(), "downloads", str(message.chat.id))
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        thumb_image_path = f"{output_directory}.jpg"
        im.save(thumb_image_path, "jpeg")
        await message.reply_photo(thumb_image_path, caption=title, reply_markup=buttons)
        await sentm.delete()
    except Exception as e:
        print(e)
        try:
            thumbnail_url = "https://telegra.ph/file/ce37f8203e1903feed544.png"
            await message.reply_photo(thumbnail_url, caption=title, reply_markup=buttons)
        except Exception as e:
            await sentm.edit(f"<code>{e}</code> #Error")
