import telegram
from telegram.ext import Updater, CommandHandler
import openai
import os

# Встановлення token бота та повідомлень від openai
TOKEN = "5918531548:AAF0TSyU4ZCWf233cAJrVcmqHnQOtKgOn2s"
openai.api_key = os.getenv("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")

# Створення бота
bot = telegram.Bot(token=TOKEN)

# Налаштування оновлень
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Функція, яка виконується при натисканні на кнопку /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вітаємо! Натисніть на кнопку «Запустити ГПТ», щоб почати запуск ГПТ від OpenAI у вашому боті!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def handle_message(update, context):
    message = update.message.text
    # do something with the message
    context.bot.send_message(chat_id=update.effective_chat.id, text="I received your message!")

message_handler = CommandHandler('handle_message', handle_message)
dispatcher.add_handler(message_handler)

# Функція, яка виконується при натиснанні на кнопку «Запустити ГПТ»
def openai_gpt(update, context):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Це тестовий запит для ГПТ від OpenAI.",
        temperature=0.5,
        max_tokens=1024,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )

# def openai_gpt(update, context):
#     user_message = " ".join(context.args)
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"You: {user_message}",
#         temperature=0.5,
#         max_tokens=1024,
#         top_p=1.0,
#         frequency_penalty=0.5,
#         presence_penalty=0.0,
#         stop=["You:"]
#     )

    context.bot.send_message(chat_id=update.effective_chat.id, text=response.choices[0].text)

openai_gpt_handler = CommandHandler('openai_gpt', openai_gpt)
dispatcher.add_handler(openai_gpt_handler)


# Запуск бота
updater.start_polling()