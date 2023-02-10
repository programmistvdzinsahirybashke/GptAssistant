import time
import openai
import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types, asyncio_filters
from telebot.asyncio_handler_backends import State, StatesGroup
import configure

openai.api_key = configure.config["GPT"]
bot = AsyncTeleBot(configure.config["token"])

bot.add_custom_filter(telebot.asyncio_filters.TextMatchFilter())
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(asyncio_filters.ChatFilter())


class UserState(StatesGroup):
    prompt = State()


@bot.message_handler(commands=["start"])
async def start(message, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("New request for GPT")
    button2 = types.KeyboardButton("Help")
    markup.add(button1, button2)
    await bot.reply_to(message, text='Hi, this is a bot with which you can make requests for ChatGPT directly from '
                                     'your Telegram!', reply_markup=markup)


@bot.message_handler(text=['New request for GPT'])
async def make_request(message):
    await bot.send_message(message.chat.id, 'Enter your request :')
    await bot.set_state(message.from_user.id, UserState.prompt, message.chat.id)


@bot.message_handler(state=UserState.prompt)
async def send_response(message):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['prompt'] = message.text
        prompt = data['prompt']
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
        print(response['choices'][0]['text'])
        await bot.reply_to(message, response['choices'][0]['text'])
        await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(text=['Help'])
async def request_group(message):
    await bot.send_message(message.chat.id, """"This is a bot that sends your request to the AI "text-davinci-003" 
    and you get a response from it in the form of a message. To start, click the "New Request for GPT" button. Before 
    each request, click this button. """)


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(bot.polling(skip_pending=True))
        except Exception as e:
            telebot.logger.error(e)
            time.sleep(15)
