# Подключен к OpenAI к Chat
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import API_KEY, TOKEN

openai.api_key = API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Сообщение приветствия, которое будет отправляться новым пользователям
WELCOME_MESSAGE = (
    "Добро пожаловать в нашего чат-бота! Как я могу Вам помочь? Напишите /help для получения списка доступных команд."
)

# Сообщение помощи, которое будет отправляться при запросе /help
HELP_MESSAGE = "Список доступных команд:\n /help - открыть это меню\n /info - получить информацию о боте\n /about - узнать больше о боте"

# Сообщение помощи, которое будет отправляться при запросе /info
INFO_MESSAGE = """GPT Chat (Generative Pre-trained Transformer Chat) - это инструмент для общения с компьютером при помощи естественного языка.
GPT Chat основан на модели искусственного интеллекта, обученной на большом количестве текстовых данных и способен генерировать ответы на заданные вопросы или комментарии пользователя.\n
GPT Chat может быть использован для различных целей, таких как:\n
1. Клиентская поддержка: GPT Chat может использоваться для ответа на вопросы клиентов и обработки запросов на поддержку в режиме реального времени.
2. Обучение и образование: GPT Chat может использоваться для создания образовательных чат-ботов, которые могут обучать людей на определенные темы.
3. Развлечение: GPT Chat может использоваться для создания чат-ботов, которые могут развлекать пользователей, например, отвечая на забавные вопросы или играя в игры.
4. Маркетинг и продажи: GPT Chat может использоваться для автоматической обработки запросов на продажу, ответов на вопросы покупателей и т.д.
5. Исследование: GPT Chat может использоваться для сбора данных и анализа мнений пользователей.\n
Кроме того, GPT Chat может быть использован для создания различных других приложений, связанных с обработкой естественного языка, в том числе синтеза речи, перевода текста и анализа тональности."""

# Сообщение помощи, которое будет отправляться при запросе /about
ABOUT_MESSAGE = "О боте:\n Языковая модель: text-davinci-003\n Телеграм бот: aiogram"


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_command_handler(message: types.Message):
    await message.answer(WELCOME_MESSAGE)


# Обработчик команды /help
@dp.message_handler(commands=["help"])
async def help_command_handler(message: types.Message):
    await message.answer(HELP_MESSAGE)


# Обработчик команды /about
@dp.message_handler(commands=["info"])
async def info_command_handler(message: types.Message):
    await message.answer(INFO_MESSAGE)


# Обработчик команды /about
@dp.message_handler(commands=["about"])
async def about_command_handler(message: types.Message):
    await message.answer(ABOUT_MESSAGE)


# Обработчик всех остальных сообщений от пользователя
@dp.message_handler()
async def send(message: types.Message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["AI:"],
    )
    await message.answer(response["choices"][0]["text"])


executor.start_polling(dp, skip_updates=True)
