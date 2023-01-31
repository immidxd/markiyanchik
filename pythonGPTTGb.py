import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from transformers import AutoModelWithLMHead, AutoTokenizer

# Конфигурация бота
token = '5918531548:AAF0TSyU4ZCWf233cAJrVcmqHnQOtKgOn2s'

# Включить логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO)

logger = logging.getLogger(__name__)

# Загрузка модели GPT-3
model = AutoModelWithLMHead.from_pretrained("openai-gpt")
tokenizer = AutoTokenizer.from_pretrained("openai-gpt")

def start(update, context):
"""Send a message when the command /start is issued."""
update.message.reply_text('Приветствую! Я GPT-3 Telegram бот. Присылайте сообщения и я буду пытаться их запомнить.')

def respond(update, context):
"""Send a response when a message is sent to the bot"""

# Получить введенный текст
text = update.message.text

# Предсказать ответ
input_ids = tokenizer.encode(text)
outputs = model.generate(input_ids)
reply_text = tokenizer.decode(outputs[0])

# Отправить ответ
update.message.reply_text(reply_text)

def main():
# Создать бота и обработчики
updater = Updater(token, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.text, respond))

# Запустить прием и обработку сообщений
updater.start_polling()

# Когда бот закончит работу, остановить прием сообщений
updater.idle()

if __name__ == '__main__':
main()