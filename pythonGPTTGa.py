import openai
import teleBot

openai.api_key = "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"
bot = telebot.TeleBot("5918531548:AAF0TSyU4ZCWf233cAJrVcmqHnQOtKgOn2s")

@bot.message_handler(func=lambda _: True)
def handle_message(message):
    print(message.text)

    # Send the message text to OpenAI for processing
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=(f"{message_text}\n"),
        temperature=0.5,
        max_tokens=2048,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )

print(response['choices'][0]['text'])

    # Get the first response from OpenAI
    # reply_text = response.choices[0].text.strip()

    # Send the response back to the user
    # bot.send_message(chat_id=message.chat_id, text=reply_text)

# Start the bot
bot.polling()
