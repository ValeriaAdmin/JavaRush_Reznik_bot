import os
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command

from fsm.states import ChatGPTStates
from keyboards import kb_start, kb_back, ikb_celebrity, ikb_select_subject_quiz
from keyboards.callback_data import QuizData

command_router = Router()


@command_router.message(F.photo)
async def cath_photo(message: Message):
    return message.photo[-1].file_id


@command_router.message(F.text == 'GPT chat request')
@command_router.message(Command('gpt'))
async def ai_gpt_command(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
    await message.answer_photo(
        photo=photo_file,
        caption='Write your request to the Chat GPT',
        reply_markup=kb_back(),
    )
    await state.set_state(ChatGPTStates.wait_for_request)


@command_router.message(F.text == 'Finish')
@command_router.message(F.text == 'Back')
@command_router.message(Command('start'))
@command_router.callback_query(QuizData.filter(F.subject == 'quiz_back'))
async def com_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await message.answer_photo(
            photo=FSInputFile(path=os.path.join('images', 'main.jpg')),
            caption=f"Hello {message.from_user.full_name}",
            reply_markup=kb_start()
        )
    else:
        await message.bot.send_photo(
            chat_id=message.from_user.id,
            photo=FSInputFile(path=os.path.join('images', 'main.jpg')),
            caption=f"Hello {message.from_user.full_name}",
            reply_markup=kb_start()
        )


@command_router.message(Command('help'))
async def com_help(message: Message):
    await message.answer(
        text=f"Hello {message.from_user.full_name}"
    )


@command_router.message(F.text == 'Dialog with person')
@command_router.message(Command('talk'))
async def ai_talk_command(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join('images', 'talk.jpg'))
    await message.answer_photo(
        photo=photo_file,
        caption='Choose a celebrity for the dialogue',
        reply_markup=ikb_celebrity(),
    )
    await state.set_state(ChatGPTStates.wait_for_request)


@command_router.callback_query(QuizData.filter(F.button == 'select_type'))
@command_router.message(F.text == 'Quiz')
@command_router.message(Command('quiz'))
async def quiz_select_subject(message: Message):
    photo_file = FSInputFile(path=os.path.join('images', 'quiz.jpg'))
    await message.bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo_file,
        caption='Select the type',
        reply_markup=ikb_select_subject_quiz(),
    )


