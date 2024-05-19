from os import getenv
from typing import List, Union

from aiogram.filters import BaseFilter
from dotenv import load_dotenv, find_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

load_dotenv(find_dotenv())
BOT_TOKEN = getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

admin_id = 198685526  # Мой tg id
blocked_users = []  # Имитация БД
bad_words_list = ['негр', 'черномазый', 'сникерс', 'уголек', 'обезьяна']

"""
/start -> Итак, вы готовы к опросу? (inline кнопка "Да") -> "Что вы думаете о других рассах?"

- запрещенные слова -> "до свидания" + в бан + прокидываем плохие слова в хендлер и отправляем админу инфу 
- гуд — спасибо, ваш ответ очень важен для нас 
"""


class BlockedUsers(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not (message.from_user.id in blocked_users)


class BadWords(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, dict[str, list[str]]]:
        words = []
        for word in message.text.split():
            if word.lower() in bad_words_list:
                words.append(word.lower())
        if words:
            return {'bad_words': words}
        else:
            return False


@dp.message(F.text == '/start', BlockedUsers())
async def greetings(message: Message):
    kb = [[InlineKeyboardButton(text='Да', callback_data='start_survey')]]
    await message.answer(text='Добро пожаловать на самый толерантный опрос в мире. Вы готовы приступить к опросу?',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=kb, resize_keyboard=True))


@dp.callback_query(F.data == 'start_survey', BlockedUsers())
async def start_survey(callback: CallbackQuery):
    await callback.message.answer(text='Итак, приступим! Расскажите о своем отношении к другим расам.')


@dp.message(BadWords(), BlockedUsers())
async def bad_answer(message: Message, bad_words: Union[bool, List[str]]):
    global blocked_users
    blocked_users.append(message.from_user.id)
    await message.answer('Вы больше не можете принимать участие в опросах. До свидания')
    await message.bot.send_message(chat_id=admin_id,
                                   text=f'Негодяй (@{message.from_user.username}) использовал ужасные слова!\n'
                                        f'Слова: <i>{", ".join(bad_words)}</i>',
                                   parse_mode='html')


@dp.message(BlockedUsers())
async def process_answer(message: Message):
    await message.answer('Спасибо ваш ответ принят')
    await message.bot.send_message(chat_id=admin_id,
                                   text=f'Новый ответ!\n'
                                        f'Ответ: <i>{message.text}</i>',
                                   parse_mode='html')


if __name__ == '__main__':
    dp.run_polling(bot)
