from aiogram import types
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app import *
from mailing.mailing_keyboard import *
from time import sleep

class Mailing(StatesGroup):
    message = State()
    message_txt = State()
    photo = State()


@dp.callback_query_handler(text='stop', state=[Mailing.photo, Mailing.message, Mailing.message_txt])
async def cancel_mailing(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    # await bot.send_message(call.from_user.id, 'Отменено', reply_markup = mailing_delete)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('mailing'))
async def process_callback_mailing(callback_query: types.CallbackQuery):
    if callback_query.from_user.id in ADMIN_ID:
        if callback_query.data == "mailing_text":
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Введите текст рассылки", reply_markup = mailing_otmena)
            await Mailing.message_txt.set()
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        elif callback_query.data == "mailing_photo":
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Отправьте фото которое хотите отправить", reply_markup = mailing_otmena)
            await Mailing.photo.set()
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    else:
        return


@dp.message_handler(content_types=['photo'], state=Mailing.photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await bot.send_message(message.chat.id, "Введите описание для фото", reply_markup = mailing_otmena)
    await Mailing.message.set()



@dp.message_handler(state=Mailing.message)
async def get_caption(message: types.Message, state: FSMContext):
    caption = message.text
    data = await state.get_data()
    subscriptions = db.get_subscriptions()
    photo = data['photo_id']
    for user in subscriptions:
        if photo != None:
            await bot.send_photo(user, photo=data['photo_id'], caption=caption, reply_markup=kb_groups)
        else:
            await bot.send_message(user, data['message'], reply_markup=kb_groups)
    await state.finish()

@dp.message_handler(state=Mailing.message_txt)
async def get_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    data = await state.get_data()
    subscriptions = db.get_subscriptions()
    for user in subscriptions:
        await bot.send_message(user, data['message'], reply_markup=kb_groups)
    await state.finish()