import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "VideoRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

DOWNLOAD_DIR = "downloads"
THUMB_DIR = "thumbnails"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)

user_data = {}

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "🎬 Professional Video Rename Bot\n\n"
        "1️⃣ Send video (max 2GB)\n"
        "2️⃣ Send new file name\n"
        "3️⃣ Send thumbnail (optional)"
    )

@app.on_message(filters.video)
async def receive_video(client, message: Message):
    user_data[message.from_user.id] = {
        "video": message.video,
        "thumb": None
    }
    await message.reply_text("✏️ Send new file name (without .mp4)")

@app.on_message(filters.photo)
async def receive_thumb(client, message: Message):
    uid = message.from_user.id
    if uid in user_data:
        thumb_path = await message.download(
            file_name=f"{THUMB_DIR}/{uid}.jpg"
        )
        user_data[uid]["thumb"] = thumb_path
        await message.reply_text("✅ Thumbnail saved")

@app.on_message(filters.text)
async def rename_video(client, message: Message):
    uid = message.from_user.id
    if uid not in user_data:
        return

    new_name = message.text.strip() + ".mp4"
    video = user_data[uid]["video"]
    thumb = user_data[uid]["thumb"]

    await message.reply_text("⏳ Processing video, please wait...")

    video_path = await client.download_media(
        video,
        file_name=os.path.join(DOWNLOAD_DIR, new_name)
    )

    await client.send_video(
        chat_id=message.chat.id,
        video=video_path,
        thumb=thumb,
        caption=f"✅ Renamed Successfully\n📁 {new_name}",
        supports_streaming=True
    )

    try:
        os.remove(video_path)
        if thumb:
            os.remove(thumb)
    except:
        pass

    user_data.pop(uid, None)

app.run()
