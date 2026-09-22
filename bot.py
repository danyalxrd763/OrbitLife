from aiogram import Bot, Dispatcher

from handlers.start import router as start_router
from handlers.router import router as core_router

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(core_router)
