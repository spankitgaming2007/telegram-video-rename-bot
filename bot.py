import os
os.remove(thumb)
user_data.pop(uid)


app.run()
```python
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


@app.on_message(filters.video)
async def receive_video(client, message: Message):
user_data[message.from_user.id] = {
"file_id": message.video.file_id,
"video": message.video,
"thumb": None
}
await message.reply_text("✏️ **New file name bhejo (without extension)**")


@app.on_message(filters.photo)
async def receive_thumb(client, message: Message):
uid = message.from_user.id
if uid in user_data:
path = await message.download(file_name=f"{THUMB_DIR}/{uid}.jpg")
user_data[uid]["thumb"] = path
await message.reply_text("✅ Thumbnail saved. Ab file name bhejo")


@app.on_message(filters.text)
async def rename_video(client, message: Message):
uid = message.from_user.id
if uid not in user_data:
return


new_name = message.text + ".mp4"
video = user_data[uid]["video"]
thumb = user_data[uid]["thumb"]


await message.reply_text("⏳ Processing...")


video_path = await client.download_media(video, file_name=new_name)


await client.send_video(
chat_id=message.chat.id,
video=video_path,
thumb=thumb,
caption=f"✅ Renamed: {new_name}",
supports_streaming=True
)


os.remove(video_path)
if thumb:
os.remove(thumb)
user_data.pop(uid)


app.run()