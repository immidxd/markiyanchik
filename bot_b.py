import random
import telegram
from telegram.ext import Updater, CommandHandler

words_list = ["I apologize for the confusion — перепрошую за плутанину", "same as always — как всегда", "beats me — без понятия", 
"let me check on that - я уточню этот вопрос", "let me check on that - я уточню этот вопрос", "I suppose so — полагаю, что так", 
"poor you — бедный (бедняга)", "freak out — cходить с ума / беситься", "it’s a piece of cake — это совсем просто!", 
"I see your point, but… — я понимаю вашу точку зрения, но…"]

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Так блет, тут мы будет учить блядские слова. Тыкай /test для проверки знаний.")

def daily_words(update, context):
    """Send a message with 10 new words every day."""
    daily_words_list = random.sample(words_list, 10)
    update.message.reply_text("Today's words: \n" + "\n".join(daily_words_list))

def test(update, context):
    """Test the user's vocabulary with a random word from the words list."""
    random_word = random.choice(words_list)
    update.message.reply_text("What is the meaning of the word " + random_word + "?")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5918531548:AAF0TSyU4ZCWf233cAJrVcmqHnQOtKgOn2s", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("daily", daily_words))
    dp.add_handler(CommandHandler("test", test))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
