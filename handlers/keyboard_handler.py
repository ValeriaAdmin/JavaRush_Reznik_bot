from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.reply_keyboards import kb_back

keyboard_router = Router()


@keyboard_router.message(F.text == 'ChatGPT')
async def kb_chatgpt(message: Message):
    await message.answer(
        text="Here...",
        reply_markup=kb_back(),
    )


@keyboard_router.message(Command('random'))
@keyboard_router.message(F.text == 'Random fact')
async def kb_chatgpt(message: Message):
    await message.answer(
        text="Here...random fact",
        reply_markup=kb_back(),
    )
