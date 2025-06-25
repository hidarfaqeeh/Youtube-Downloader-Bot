import asyncio
import os
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.ffmfunc import duration
from helper.ytdlfunc import downloadvideocli, downloadaudiocli
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

@Client.on_callback_query()
async def catch_youtube_fmtid(client, callback_query):
    cb_data = callback_query.data
    if cb_data.startswith("ytdata||"):
        yturl = cb_data.split("||")[-1]
        format_id = cb_data.split("||")[-2]
        media_type = cb_data.split("||")[-3].strip()
        print(media_type)
        if media_type == 'audio':
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Audio", callback_data=f"{media_type}||{format_id}||{yturl}"),
                 InlineKeyboardButton("Document", callback_data=f"docaudio||{format_id}||{yturl}")]
            ])
        else:
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Video", callback_data=f"{media_type}||{format_id}||{yturl}"),
                 InlineKeyboardButton("Document", callback_data=f"docvideo||{format_id}||{yturl}")]
            ])
        await callback_query.edit_message_reply_markup(reply_markup=buttons)

@Client.on_callback_query()
async def catch_youtube_dldata(client, callback_query):
    cb_data = callback_query.data.strip()
    yturl = cb_data.split("||")[-1]
    format_id = cb_data.split("||")[-2]
    thumb_image_path = os.path.join(os.getcwd(), "downloads", f"{callback_query.message.chat.id}.jpg")
    if os.path.exists(thumb_image_path):
        width, height = 0, 0
        metadata = extractMetadata(createParser(thumb_image_path))
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        img = Image.open(thumb_image_path)
        if cb_data.startswith(("audio", "docaudio", "docvideo")):
            img = img.resize((320, height))
        else:
            img = img.resize((90, height))
        img.save(thumb_image_path, "JPEG")
    if not cb_data.startswith(("video", "audio", "docaudio", "docvideo")):
        print("no data found")
        return
    filext = "%(title)s.%(ext)s"
    userdir = os.path.join(os.getcwd(), "downloads", str(callback_query.message.chat.id))
    if not os.path.isdir(userdir):
        os.makedirs(userdir)
    await callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup([[InlineKeyboardButton("Downloading...", callback_data="down")]])
    )
    filepath = os.path.join(userdir, filext)
    audio_command = [
        "yt-dlp",
        "-c",
        "--prefer-ffmpeg",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", format_id,
        "-o", filepath,
        yturl,
    ]
    video_command = [
        "yt-dlp",
        "-c",
        "--no-playlist",
        "-f", format_id,
        "-o", filepath,
        yturl,
    ]
    # هنا يمكنك الاختيار حسب نوع الميديا وتنفيذ التنزيل المناسب
