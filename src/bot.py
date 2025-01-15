import telebot
import logging
from groq import Groq

#bot id : @example202_bot


logging.basicConfig(level=logging.DEBUG)


bot = telebot.TeleBot('7913870753:AAEMGvU9kKT9GCRNjg-1iCeDZEKGIq37c0Y')
client = Groq(api_key="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")


model = "llama3-groq-70b-8192-tool-use-preview"
messages = [{"role": "system", "content": "ChatBot"}]


first_button = telebot.types.InlineKeyboardButton("Download", url='https://example.com/download')
second_button = telebot.types.InlineKeyboardButton("Tell Me", url='https://t.me/ItsMhsa_82')

markup = telebot.types.InlineKeyboardMarkup()
markup.add(first_button)

markup2 = telebot.types.InlineKeyboardMarkup()
markup2.add(second_button)

#-------------------------------------------START--------------------------------------------------------------

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome to the chatbot! Use /chat to talk to me or /help to get support.")


#---------------------------------------------HELP------------------------------------------------------------

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Click below to get help or contact support:", reply_markup=markup2)


#----------------------------------------------CHAT-----------------------------------------------------------

@bot.message_handler(commands=['chat'])
def handle_chat(message):
    bot.send_message(message.chat.id, "Hi! I'm ready to chat with you. What do you want to talk about?")
    bot.send_message(message.chat.id, "Type 'bye' to quit.")


@bot.message_handler(func=lambda message: True)
def handle_prompt(message):
    prompt = message.text.strip()
    
    
    if prompt.lower() == "bye":
        bot.reply_to(message, "Goodbye! 👋")
        return

    
    messages.append({"role": "user", "content": prompt})

    try:
        # Send the prompt to the Groq model
        completion = client.chat.completions.create(
            model=model,
            messages=messages
        )

        # Get the assistant's response
        assistant_response = completion.choices[0].message.content

        # Append the assistant's response to the conversation history
        messages.append({"role": "assistant", "content": assistant_response})

        
        bot.reply_to(message, assistant_response)

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        bot.reply_to(message, f"Sorry, something went wrong: {e}")


bot.polling(non_stop=True)
