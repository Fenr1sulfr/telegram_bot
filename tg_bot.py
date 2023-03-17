from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import  executor
import os
from getAnswer import getAnswer


bot=Bot(token=os.getenv('TOKEN'))
dp=Dispatcher(bot)
grant=getAnswer('A1')
aet=getAnswer('D1')

@dp.message_handler()
async def echo_send(message:types.Message):

    #await message.answer(grant)
    if(message.text=="AET"):
        await message.reply_to_message(aet)
   # await message.reply(message.text)
   # await bot.send_message(message.from_user.id, message.text)

executor.start_polling(dp,skip_updates=True)


