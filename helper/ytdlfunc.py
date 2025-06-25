from pyrogram.types import InlineKeyboardButton
from utils.util import humanbytes
from yt_dlp import YoutubeDL
import asyncio

def buttonmap(item):
    quality = item["format"]
    if "audio" in quality:
        return [InlineKeyboardButton(f"{quality} 🎵 {humanbytes(item['filesize'])}",
                                     callback_data=f"ytdata||audio||{item['format_id']}||{item['yturl']}")]
    else:
        return [InlineKeyboardButton(f"{quality} 📹 {humanbytes(item['filesize'])}",
                                     callback_data=f"ytdata||video||{item['format_id']}||{item['yturl']}")]

def create_buttons(quality_list):
    return map(buttonmap, quality_list)

def extractYt(yturl):
    ydl = YoutubeDL()
    with ydl:
        qualityList = []
        r = ydl.extract_info(yturl, download=False)
        for format in r["formats"]:
            if not "dash" in str(format["format"]).lower():
                qualityList.append({
                    "format": format["format"],
                    "filesize": format.get("filesize", 0),
                    "format_id": format["format_id"],
                    "yturl": yturl
                })
        return r["title"], r["thumbnail"], qualityList

async def downloadvideocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    filename = t_response.split('Merging formats into')[-1].split('"')[1]
    return filename

async def downloadaudiocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print("Download error:", e_response)
    return t_response.split("Destination")[-1].split("Deleting")[0].split(":")[-1].strip()
