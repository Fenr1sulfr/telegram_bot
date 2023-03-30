import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from infos.ops import *
from infos.faq import *
from infos.aet import *
from infos.ent import *


global_kb = types.InlineKeyboardMarkup()
global_kb_back = types.InlineKeyboardButton(text="Назад", callback_data="back")
global_kb_back_op = types.InlineKeyboardButton(text="Назад", callback_data="OP")
global_kb_back_gop = types.InlineKeyboardButton(text="Назад", callback_data="GOP")
global_kb_back_faq = types.InlineKeyboardButton(text="Назад", callback_data='faq')
global_kb_back_aet = types.InlineKeyboardButton(text="Назад", callback_data="aet")
global_kb_back_ent = types.InlineKeyboardButton(text="Назад", callback_data="ent")


info = {
    'aet': f'{aet}',
    'ent': f'{ent}',
    'zhata': f'{zhata}'
}

aet_info = {
    'aet_money': f'{aet_money}',
    'aet_certificate': f'{aet_certificate}',
    'aet_material': f'{aet_material}'
}

gop = {
    'it': f'{soft}\n\n{media}\n\n{math}\n\n{comp}\n\n{bigdata}',
    'cs': f'{cyber}',
    'com': f'{smart}',
    'iiot': f'{iiot}',
    'management': f'{itm}\n\n{ite}\n\n{dpas}',
    'dj': f'{dj}'
}

ops = {
    'SE': f'{soft}',
    'MT': f'{media}',
    'CS': f'{cyber}',
    'IT': f'{comp}',
    'BDA': f'{bigdata}',
    'MCS': f'{math}',
    'ST': f'{smart}',
    'IIOT': f'{iiot}',
    'ITM': f'{itm}',
    'ITE': f'{ite}',
    'DPAS': f'{dpas}',
    'DJ': f'{dj}'
}

ent_info = {
    'ent_2020': f'{ent_2020}',
    'ent_2021': f'{ent_2021}',
    'ent_2022': f'{ent_2022}'
}





# @dp.callback_query_handler(lambda call: call.data in ['SE', 'MT', 'IT', 'MCS', 'BDA', 'CS'])
# async def opshki(call: types.CallbackQuery):
#     keyboard = InlineKeyboardMarkup()
#     keyboard.add(global_kb_back_op)
#     key = call.data
#     await call.message.edit_text(f"{ops[key]}", reply_markup=keyboard, parse_mode = 'HTML')