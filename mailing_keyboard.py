from aiogram import types

#Для рассылки
kb_groups = types.InlineKeyboardMarkup()
abit = types.InlineKeyboardButton(text="Официальный чат", url="https://t.me/+aVJNC7bmXQc4YzAy")
site = types.InlineKeyboardButton(text="Официальный сайт", url="https://astanait.edu.kz")
flud = types.InlineKeyboardButton(text="Флуд чат", url="https://t.me/+8vj6tA0UQ8hkZGUy")

kb_groups.add(abit, flud)
kb_groups.add(site)

#хз
rickroll = types.InlineKeyboardMarkup()
rickroll_1 = types.InlineKeyboardButton(text="иди нахуй", url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
rickroll.add(rickroll_1)


#Клава для рассылки
kb_mailing = types.InlineKeyboardMarkup(row_width=2)
btn_text = types.InlineKeyboardButton(text="Только текст", callback_data="mailing_text")
btn_photo = types.InlineKeyboardButton(text="Текст с фото", callback_data="mailing_photo")
kb_mailing.add(btn_text, btn_photo)