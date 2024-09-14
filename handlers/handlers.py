import time
from datetime import datetime
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboards import inline_keyboard
from database import database as db
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from script import ParseSourcesTg
import asyncio
from loguru import logger
import random
import os

router = Router()

class AddSource(StatesGroup):
    url = State()


@router.message(CommandStart())
async def start(message: Message):
    db.add_user(message.from_user.id, message.from_user.username)
    await message.bot.send_photo(message.chat.id,
                                 photo=FSInputFile('bitcoin-logo.jpg'),
                                 caption='Привет <b>Глеб</b> и <b>Матвей</b>. \nТут вы можете подтверждать или отклонять новости, которые я сплагиачу для вас😁.',
                                 reply_markup=inline_keyboard.create_inline_kb(1, 'Добавить источники', 'Новости'))


@router.callback_query(F.data == 'Новости')
async def send_news(callback: CallbackQuery):
    await callback.message.answer('<b>Ожидайте...</b>\nСобираю для вас последние новости из всех источников⚠')

    parser = ParseSourcesTg()
    parser.gpt_request()
        # await callback.message.answer('Произошла ошибка ⚠️.\n<b>Повторите нажатие</b>')
        # logger.error(ex)
        # db.clear_news_table()
    news = db.select_news_gpt()
    imgs = db.select_news()
    for i in range(len(news)):
        try:
            await callback.message.bot.send_photo(chat_id=1190679768, photo=imgs[i][2],
                                                caption=f'<b>Источник</b>: {news[i][0]}\n<b>Отредактированная новость</b>: {news[i][1]}',
                                                reply_markup=inline_keyboard.create_inline_kb(1, 'Опубликовать',
                                                                                              'Не публиковать'))
            await callback.message.bot.send_photo(chat_id=871709880, photo=imgs[i][2],
                                                caption=f'<b>Источник</b>: {news[i][0]}\n<b>Отредактированная новость</b>: {news[i][1]}',
                                                reply_markup=inline_keyboard.create_inline_kb(1, 'Опубликовать',
                                                                                              'Не публиковать'))
        except Exception as ex:
            logger.error(ex)
            await callback.message.answer(text = 'Сообщение из чата прочиталось некорректно', reply_markup=inline_keyboard.create_inline_kb(1, 'Удалить'))
    db.clear_news_gpt()
    db.clear_news_table()

@router.callback_query(F.data == 'Удалить')
async def no_public(callback: CallbackQuery):
    await callback.message.delete(inline_message_id=callback.inline_message_id)

@router.callback_query(F.data == 'Не публиковать')
async def no_public(callback: CallbackQuery):
    await callback.message.delete(inline_message_id=callback.inline_message_id)

@router.callback_query(F.data == 'Опубликовать')
async def public(callback: CallbackQuery):
    text = callback.message.caption.split('\n')[1].replace('Отредактированная новость: ', '')
    photo = callback.message.photo[0].file_id
    await callback.message.bot.send_photo(chat_id=-1001745374968, photo=photo, caption = '<b>💲Криптовалюта - Арбитраж💲</b>\n\n' + text)
    await callback.message.delete()


@router.callback_query(StateFilter(None), F.data == 'Добавить источники')
async def add_source(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите ссылку для добавления')
    await state.set_state(AddSource.url)

@router.message(AddSource.url, F.text)
async def add_source1(message: Message, state:FSMContext):
    await state.update_data(url = message.text)
    data = await state.get_data()
    db.add_source(data['url'])
    await message.answer('<b>Источник добавлен</b>')
    await state.clear()



