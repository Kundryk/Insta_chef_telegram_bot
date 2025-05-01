import logging
import os
import requests
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, CHANNEL_ID

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def transcribe_audio(file_path):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    files = {
        "file": (os.path.basename(file_path), open(file_path, "rb"), "audio/mp4"),
        "model": (None, "whisper-1")
    }
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        return response.json().get("text")
    else:
        logging.error(f"Transcription error: {response.text}")
        return None

@dp.channel_post_handler(content_types=['video'])
async def handle_channel_video(message: types.Message):
    if str(message.chat.id) == CHANNEL_ID:
        logging.info("Отримано відео з каналу!")
        file_id = message.video.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        local_file = f"temp_{file_id}.mp4"
        await bot.download_file(file_path, local_file)
        logging.info("Відео завантажено, відправляю на транскрипцію...")
        transcript = await transcribe_audio(local_file)
        if transcript:
            logging.info(f"Транскрипція: {transcript}")
        else:
            logging.info("Не вдалося отримати транскрипцію.")
        os.remove(local_file)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
