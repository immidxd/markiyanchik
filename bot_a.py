import json
import os
import random
import telegram
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler

TELEGRAM_API_KEY = "5918531548:AAF0TSyU4ZCWf233cAJrVcmqHnQOtKgOn2s"

# Define the conversation states
ADD_WORD, STUDY_WORDS = range(2)

def add_word_input(update, context):
    """Handle the input of a new word and its translation."""
    word_input = update.message.text.strip().split("-")
    if len(word_input) == 2:
        word, translation = word_input
        word = word.strip()
        translation = translation.strip()
        # Validate the input
        if not word or not translation:
            update.message.reply_text("Invalid input. Please send a valid word and translation.")
            return ADD_WORD
        # Save the new word to the vocabulary list
        try:
            with open("vocabulary.json", "r") as f:
                vocabulary = json.load(f)
        except:
            vocabulary = []
        vocabulary.append({"word": word, "translation": translation})
        with open("vocabulary.json", "w") as f:
            json.dump(vocabulary, f, ensure_ascii=False, indent=4)
        update.message.reply_text("The word has been added to the vocabulary list.")
        return ConversationHandler.END
    else:
        update.message.reply_text("Invalid input. Please send the word and translation in the following format: "
                                  "word - translation")
        return ADD_WORD

def study_words(update, context):
    """Send 10 random words from the vocabulary list for studying."""
    try:
        with open("vocabulary.json", "r") as f:
            vocabulary = json.load(f)
    except:
        update.message.reply_text("No words found to study.")
        return
    words = random.sample(vocabulary, 10)
    for word in words:
        update.message.reply_text(f"{word['word']} - {word['translation']}")

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Welcome to the English vocabulary bot! Please select an option:")
    # Create the inline keyboard
    keyboard = [
        [InlineKeyboardButton("Add new word", callback_data="add_word")],
        [InlineKeyboardButton("Study words", callback_data="study_words")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please select an option:", reply_markup=reply_markup)

def callback_query(update, context):
    """Handle callback query for the inline keyboard."""
    query = update.callback_query
    if query.data == "add_word":
        query.edit_message_text(text="Please send me the word and its translation in the following format: "
                                 "word - translation")
        return ADD_WORD
    elif query.data == "study_words":
        study_words(update, context)
    else:
        query.answer()

def cancel(update, context):
    """Handle canceling of the conversation."""
    update.message.reply_text("The operation has been canceled.")
    return ConversationHandler.END

def main():
    """Start the bot."""
    # Read the API key from an environment variable
    TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
    # Initialize the Telegram bot

bot = telegram.Bot(token=TELEGRAM_API_KEY)
update_queue = asyncio.Queue()
updater = telegram.ext.Updater(bot=bot, update_queue=update_queue)

# Add handlers
updater = Updater(TELEGRAM_API_KEY, use_context=True)
bot = telegram.Bot(TELEGRAM_API_KEY)
app = Application(bot,updater)

# Add the conversation handler
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add_word_input)],
    states={
        ADD_WORD: [MessageHandler(Filters.text, add_word_input)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
app.add_handler(conversation_handler)

# Add the study words handler
app.add_handler(CommandHandler("study", study_words))
app.add_handler(MessageHandler(Filters.TEXT, check_answer))

# Add the start command handler
app.add_handler(CommandHandler("start", start))

# Start the bot
updater.start_polling()
updater.idle()

        


