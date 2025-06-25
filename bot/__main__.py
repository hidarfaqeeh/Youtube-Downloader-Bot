from pyrogram import Client
import config

DOWNLOAD_LOCATION = "./downloads"
BOT_TOKEN = config.BOT_TOKEN
APP_ID = config.APP_ID
API_HASH = config.API_HASH

plugins = dict(root="plugins")

app = Client(
    "YouTubeDlBot",
    bot_token=BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    plugins=plugins,
    workers=100
)

if __name__ == "__main__":
    app.run()
