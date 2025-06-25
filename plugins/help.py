from pyrogram import Client, filters

@Client.on_message(filters.command(["help"]))
async def help_command(client, message):
    helptxt = "البوت يدعم تحميل فيديو واحد فقط من يوتيوب (لا يدعم قائمة التشغيل). فقط أرسل رابط يوتيوب!"
    await message.reply_text(helptxt)
