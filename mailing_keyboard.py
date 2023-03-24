from aiogram import types

#Для рассылки
kb_groups = types.InlineKeyboardMarkup()
abit = types.InlineKeyboardButton(text="Официальный чат", url="https://t.me/+aVJNC7bmXQc4YzAy")
site = types.InlineKeyboardButton(text="Официальный сайт", url="https://astanait.edu.kz")
flud = types.InlineKeyboardButton(text="Флуд чат", url="https://t.me/+8vj6tA0UQ8hkZGUy")

kb_groups.add(abit, flud)
kb_groups.add(site)


#Клава для рассылки
kb_mailing = types.InlineKeyboardMarkup(row_width=2)
btn_text = types.InlineKeyboardButton(text="Только текст", callback_data="mailing_text")
btn_photo = types.InlineKeyboardButton(text="Текст с фото", callback_data="mailing_photo")
kb_mailing.add(btn_text, btn_photo)

mailing_otmena = types.InlineKeyboardMarkup()
otmena = types.InlineKeyboardButton(text="Отменить", callback_data="stop")
mailing_otmena.add(otmena)

delete = types.InlineKeyboardMarkup()
delete1 = types.InlineKeyboardButton(text="Удалить", callback_data="delete")
delete.add(delete1)


admin = types.InlineKeyboardMarkup()
help1 = types.InlineKeyboardButton(text="Инструкция для админов", callback_data="admin_help")
admin.add(help1)


ah_text = '''
<b>📕Инструкция для админов</b>

👤
/deanon - <u>узнать информацию о пользователе(для использования нужно ответить на сообщение пользователя)</u>

Информация выводится в таком виде:
User ID: <b>12345678</b>
Юзернейм: <b>изана.</b>
Кол-во предупреждений: <b>?</b>
Последнее предупреждение: <b>2023-03-20 21:24:41</b>
Сообщения: <b>Сообщения содержащие мат которые написал этот пользователь</b>

📣
/mailing - <u>отправка рассылки.</u>
<i>Два способа:
# Только текст
# Фото с текстом</i>
'''
