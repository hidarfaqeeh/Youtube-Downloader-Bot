from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command(["start"]))
async def start(client, message):
    joinButton = InlineKeyboardMarkup([
        [InlineKeyboardButton("Channel", url="https://t.me/aryan_bots")],
        [InlineKeyboardButton("Report Bugs 😊", url="https://t.me/aryanvikash")]
    ])
    welcomed = f"Hey <b>{message.from_user.first_name}</b>\n/help للمزيد من المعلومات"
    await message.reply_text(welcomed, reply_markup=joinButton)
