import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, CHANNEL_ID

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Обробник для всіх повідомлень у каналі
@dp.channel_post_handler(content_types=['any'])
async def handle_channel_post(message: types.Message):
    if str(message.chat.id) == CHANNEL_ID:
        # Логуємо отримання повідомлення
        logging.info(f"Отримано нове повідомлення з каналу!")

        # Якщо це відео або посилання
        if message.video or message.text:
            content = "відео" if message.video else "посилання"
            logging.info(f"Тип контенту: {content}")

            # Тут можна додати код для збереження або обробки
            if message.video:
                file_id = message.video.file_id
                logging.info(f"ID відео: {file_id}")
            if message.text:
                logging.info(f"Текст повідомлення: {message.text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
