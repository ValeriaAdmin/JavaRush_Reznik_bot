from aiogram import Router
from .ai_handlers import ai_handler
from .command_handlers import command_router
from .keyboard_handler import keyboard_router
from .callback_handlers import callback_router

all_handlers_router = Router()
all_handlers_router.include_routers(
    ai_handler,
    command_router,
    keyboard_router,
    callback_router,
)

__all__ = [
    'all_handlers_router',
]
