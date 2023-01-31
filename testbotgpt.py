import logging
import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO)
openai.api_key = "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"

def main():
    bot = Updater("5918531548:AAF0TSyU4ZCWf233cAJrVcmqHnQOtKgOn2s", use_context=True)

    dp = bot.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    logging.info("Bot started")
    bot.start_polling()
    bot.idle()


def start(update, context):
    print('/start called')
    update.message.reply_text('Dobryden, everybody 🥸\nЧо нада?')

def handle_message(update, context):
    user_id = update.message.from_user.id
    message = update.message.text
    print(message)
    update.message.reply_text('...')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        temperature=0.5,
        max_tokens=1024,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    response_text = response.choices[0].text
    update.message.reply_text(response_text)

if __name__ == '__main__':
    main()
