from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from datab import SQLighter

bot = Bot(token="5995233128:AAHD38e8sj8Mo_yCzIPlAvWUvPcQeUsHdQA")
# Диспетчер для бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
db = SQLighter('db.db')
ADMIN_ID = [448066464, 936574288]