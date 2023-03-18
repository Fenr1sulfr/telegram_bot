import asyncio
import logging
from time import sleep
import aiogram.utils.markdown as md
from aiogram import types
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import exceptions
import sqlite3
from infos import *
from getAnswer import *
import os
from djantimat.helpers import PymorphyProc


bot = Bot(token=os.getenv("TOKEN"))
# Диспетчер для бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def start(msg: types.Message):
    chat_type = msg.chat.type
    
    if chat_type != 'private': # Если это личное сообщение
        await msg.answer("Привет! Это группа блять. Напиши мне что-нибудь.")
    else:
        kb_start = types.InlineKeyboardMarkup()
        kb_start_gop = types.InlineKeyboardButton(text="Информация про ГОП", callback_data="GOP")
        kb_start_faq = types.InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data='faq')
        kb_start.add(kb_start_gop, kb_start_faq)
        await msg.answer(f"Привет, {msg.from_user.first_name}!", reply_markup=kb_start)
    # conn.close()

@dp.callback_query_handler(text="back")
async def back(call: types.CallbackQuery):
    kb_start = types.InlineKeyboardMarkup()
    kb_start_gop = types.InlineKeyboardButton(text="Информация про ГОП", callback_data="GOP")
    kb_start_faq = types.InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data='faq')
    kb_start.add(kb_start_gop, kb_start_faq)
    await call.message.edit_text("*Приветствие*!", reply_markup=kb_start)

@dp.callback_query_handler(text="GOP")
async def op(call: types.CallbackQuery):
    kb_gop = types.InlineKeyboardMarkup()
    kb_gop_it  = types.InlineKeyboardButton(text="Информационные технологии", callback_data="it")
    kb_gop_cs  = types.InlineKeyboardButton(text="Информационная безопасность", callback_data="cs")
    kb_gop_com  = types.InlineKeyboardButton(text="Коммуникации и коммуникационные технологии", callback_data="com")
    kb_gop_iiot  = types.InlineKeyboardButton(text="Электротехника и автоматизация", callback_data="iiot")
    kb_gop_management  = types.InlineKeyboardButton(text="Менеджмент и управление", callback_data="management")
    kb_gop_dj  = types.InlineKeyboardButton(text="Журналистика и репортерское дело", callback_data="dj")
    kb_gop.row(kb_gop_it, kb_gop_cs, kb_gop_com)
    kb_gop.row(kb_gop_iiot, kb_gop_management, kb_gop_dj)
    kb_gop.add(global_kb_back)
    await call.message.edit_text("Выберите ГОП про который хотите узнать: ", reply_markup=kb_gop)

@dp.callback_query_handler(lambda call: call.data in ['it', 'cs', 'com', 'iiot', 'management', 'dj'])
async def opshki(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(global_kb_back_gop)
    key = call.data
    await call.message.edit_text(f"{gop[key]}", reply_markup=keyboard, parse_mode = 'HTML')


@dp.callback_query_handler(text="faq")
async def op(call: types.CallbackQuery):
    kb_faq = types.InlineKeyboardMarkup()
    kb_faq_ent  = types.InlineKeyboardButton(text="ЕНТ | Баллы на грант", callback_data="ent")
    kb_faq_aet  = types.InlineKeyboardButton(text="АЕТ", callback_data="aet")
    kb_faq_zhata  = types.InlineKeyboardButton(text="Общежитие", callback_data="zhata")
    kb_faq.add(kb_faq_ent, kb_faq_zhata)
    kb_faq.add(kb_faq_aet)
    kb_faq.add(global_kb_back)
    await call.message.edit_text("Самые часто задаваемые вопросы", reply_markup=kb_faq)

@dp.callback_query_handler(lambda call: call.data in ['zhata'])
async def opshki(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(global_kb_back_faq)
    key = call.data
    await call.message.edit_text(f"{info[key]}", reply_markup=keyboard, parse_mode = 'HTML', disable_web_page_preview=True)

@dp.callback_query_handler(text="aet")
async def aet(call: types.CallbackQuery):
    kb_aet = types.InlineKeyboardMarkup()
    kb_aet_money = types.InlineKeyboardButton(text="Оплата АЕТа", callback_data="aet_money")
    kb_aet_material  = types.InlineKeyboardButton(text="Материалы для подготовки", callback_data="aet_material")
    kb_aet_certificate  = types.InlineKeyboardButton(text="Сертификаты", callback_data="aet_certificate")
    kb_aet.add(kb_aet_money, kb_aet_material, kb_aet_certificate)
    kb_aet.add(global_kb_back_faq)
    key = call.data
    await call.message.edit_text(f"{getAnswer('Говно', 'A1')}", reply_markup=kb_aet,parse_mode= 'HTML', disable_web_page_preview=True)


@dp.callback_query_handler(lambda call: call.data in ['aet_money', 'aet_material', 'aet_certificate'])
async def opshki(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(global_kb_back_aet)
    key = call.data
    await call.message.edit_text(f"{aet_info[key]}", reply_markup=keyboard, parse_mode = 'HTML', disable_web_page_preview=True)


@dp.callback_query_handler(text="ent")
async def aet(call: types.CallbackQuery):
    kb_ent = types.InlineKeyboardMarkup()
    kb_ent_2020 = types.InlineKeyboardButton(text="2020", callback_data="ent_2020")
    kb_ent_2021  = types.InlineKeyboardButton(text="2021", callback_data="ent_2021")
    kb_ent_2022  = types.InlineKeyboardButton(text="2022", callback_data="ent_2022")
    kb_ent.add(kb_ent_2020, kb_ent_2021, kb_ent_2022)
    kb_ent.add(global_kb_back_faq)
    key = call.data
    await call.message.edit_text(f"{getAnswer('ЕНТ', 'A1')}", reply_markup=kb_ent,parse_mode= 'HTML', disable_web_page_preview=True)

@dp.callback_query_handler(lambda call: call.data in ['ent_2020', 'ent_2021', 'ent_2022'])
async def opshki(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(global_kb_back_ent)
    key = call.data
    await call.message.edit_text(f"{ent_info[key]}", reply_markup=keyboard, parse_mode = 'HTML', disable_web_page_preview=True)
@dp.message_handler()
async def badWordsFilter(message:types.Message):
    if PymorphyProc.test(message.text):
        await bot.send_message("Иди нахуй")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)





