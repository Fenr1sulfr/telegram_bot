import asyncio
import json
import os
import time
import aiogram.utils.markdown as md
import sqlite3
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio
from aiogram.types import ParseMode
from aiogram.utils import exceptions
from time import sleep
from getAnswer import *
from app import *
from datetime import datetime, timedelta
from deanon.datab import *
from deanon.warning_db import *
from infos.infos import *
from mailing.mailing_states import *
from mailing.mailing_keyboard import *

@dp.callback_query_handler(text = "delete")
async def mailing_delete(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)

@dp.message_handler(commands='start')
async def start(msg: types.Message):
    if msg.chat.type != 'private': # Если это не личное сообщение
        await msg.answer("Данную команду нужно использовать в лс!")
    else:
        kb_start = types.InlineKeyboardMarkup()
        kb_start_gop = types.InlineKeyboardButton(text="Информация про ГОП", callback_data="GOP")
        kb_start_faq = types.InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data='faq')
        kb_start.add(kb_start_gop, kb_start_faq)
        await msg.answer(f"Привет, {msg.from_user.first_name}!", reply_markup=kb_start)
    
    if(not db.subscriber_exists(msg.from_user.id)):
        db.add_subscriber(msg.from_user.id)
    else:
        db.update_subscription(msg.from_user.id, True)


@dp.callback_query_handler(text = "admin_help")
async def admin_help(call: types.CallbackQuery):
    await call.message.edit_text(text=ah_text, reply_markup=delete, parse_mode = 'HTML')

@dp.message_handler(commands='help')
async def help(msg: types.Message):
    if msg.from_user.id in ADMIN_ID:
        if msg.chat.type != 'private':
            await msg.answer("Помощь отправлена в лс!")
            await bot.send_message(msg.from_user.id, "Основыные команды:\n/start - Начало\n/help - Получить данное сообщение", reply_markup = admin, parse_mode = 'HTML')
        else:
            await bot.send_message(msg.from_user.id, "Основыные команды:\n/start - Начало\n/help - Получить данное сообщение", reply_markup = admin, parse_mode = 'HTML')
    else:
        if msg.chat.type != 'private':
            await msg.answer("Помощь отправлена в лс!")
            await bot.send_message(msg.from_user.id, "Основыные команды:\n/start - Начало\n/help - Получить данное сообщение")
        else:
            await bot.send_message(msg.from_user.id, "Основыные команды:\n/start - Начало\n/help - Получить данное сообщение")


@dp.message_handler(commands='deanon')
async def deanon_user(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        if message.chat.type == 'private':
            await message.answer("Используйте эту команду в чате ответив на чье-то сообщение.")
        else:
            user_id = message.reply_to_message.from_user.id
            first_name = "["+message.reply_to_message.from_user.first_name+"](tg://user?id="+str(user_id)+")"
            cursor.execute("SELECT first_name, count, last_warned, message_text FROM warnings WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            if user is None:
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.send_message(message.from_user.id, text=f"User ID: *{user_id}*\nНикнейм: {first_name}\n\nНи одного нарушения на счету :)", reply_markup = delete, parse_mode="Markdown")
            else:
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.send_message(message.from_user.id, text=f"User ID: *{user_id}*\nНикнейм: {first_name}\nКол-во предупреждений: *{user[1]}*\n\nПоследнее предупреждение: *{user[2]}*\n\nСообщения:\n_{user[3]}_", reply_markup = delete, parse_mode="Markdown")
    else:
        return


@dp.message_handler(commands='mailing')
async def go(message: types.Message):
    if message.chat.type != 'private':
        return
    else:
        if message.from_user.id in ADMIN_ID:
            await message.answer("Вы хотите отправить только текст или текст с фото?", reply_markup=kb_mailing)
        else:
            return


@dp.callback_query_handler(text="back")
async def back(call: types.CallbackQuery):
    kb_start = types.InlineKeyboardMarkup()
    kb_start_gop = types.InlineKeyboardButton(text="Группы образовательных программ", callback_data="GOP")
    kb_start_faq = types.InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data='faq')
    kb_start.add(kb_start_gop)
    kb_start.add(kb_start_faq)
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


def replacing(to_escape_msg):
    escaped_msg = to_escape_msg.replace("-", "\\-").replace("+", "\\+").replace("[", "\\[").replace(".", "\\.").replace("**", "\\**")
    return escaped_msg

@dp.callback_query_handler(lambda call: call.data in ['it', 'cs', 'com', 'iiot', 'management', 'dj'])
async def opshki(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(global_kb_back_gop)
    key = call.data
    if call.data == 'it':
        start_time = time.time()
        text = ''
        text += replacing(getAnswer('ОП-шки', 'A1')) + '\n'
        await call.message.edit_text(f"{text}", reply_markup=keyboard, parse_mode='MarkdownV2')
        # end_time = time.time()
        # await call.message.answer(f"Из таблицы:\nНачало: {start_time}\nКонец: {end_time}\nВремя: {end_time - start_time}")
    if call.data == 'iiot':
        # start_time = time.time()
        await call.message.edit_text(f"{gop[call.data]}", reply_markup=keyboard, parse_mode='HTML')
        # end_time = time.time()
        # await call.message.answer(f"Из файлов:\nНачало: {start_time}\nКонец: {end_time}\nВремя: {end_time - start_time}")


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
    await call.message.edit_text(f"{getAnswer('Говно', 'A2')}", reply_markup=kb_aet,parse_mode= 'HTML', disable_web_page_preview=True)


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
async def badWordsFilter(message: types.Message):
    if message.chat.type != 'private':
        bad_words = json.load(open('badword.json'))
        text_words = {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}
        if text_words.intersection(set(bad_words)):
            user_id = message.from_user.id
            first_name = message.from_user.first_name
            message_text = message.text
            warning_count = get_warning_count(user_id)
            increment_warning_count(first_name, user_id, message_text)
            await update_sheet()
            await message.reply(f"В данном чате нельзя использовать нецензурную лексику.\nКол-во предупреждений: {warning_count + 1}")
            if warning_count + 1 >= WARNING_LIMIT:
                await warning_to_zero(user_id)
                await mute_user(message.chat.id, user_id)
                await message.reply("Ты был замучен на {} дней за использование нецензурной лексики.".format(MUTE_DURATION))
    else:
        return


async def on_startup(dp):
    from other.set_commands import set_default_commands
    await set_default_commands(dp)

if __name__ ==  '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)





