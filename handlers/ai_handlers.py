import os
import aiofiles

from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from gtts import gTTS

from keyboards import ikb_next_quiz
from keyboards.callback_data import QuizData
from keyboards.reply_keyboards import kb_random_facts, kb_start
from .command_handlers import com_start
from fsm.states import ChatGPTStates, CelebrityDialog, QuizGame
from classes import ai_client

import speech_recognition as sr
from pydub import AudioSegment

ai_handler = Router()


async def read_prompt(path: str):
    async with aiofiles.open('prompts/' + path, 'r', encoding='UTF-8') as file:
        prompt = await file.read()
    return prompt


@ai_handler.message(F.text == 'I want another fact')
@ai_handler.message(Command('random'))
@ai_handler.message(F.text == 'Random fact')
async def com_gpt(message: Message):
    prompt = await read_prompt('random.txt')
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    request_message = [
        {'role': 'user',
         'content': 'To write a random fact',
         },
    ]
    caption = await ai_client.text_request(request_message, prompt)
    photo_file = FSInputFile(path=os.path.join('images', 'random.jpg'))

    await message.answer_photo(
        photo=photo_file,
        caption=caption,
        reply_markup=kb_random_facts(),
    )


@ai_handler.message(ChatGPTStates.wait_for_request)
async def ai_gpt_request(message: Message, state: FSMContext):
    if message.text == 'Back':
        await com_start(message)
    else:
        request = message.text
        prompt = await read_prompt('gpt.txt')
        await message.bot.send_chat_action(
            chat_id=message.from_user.id,
            action=ChatAction.TYPING,
        )
        request_message = [
            {'role': 'user',
             'content': request,
             },
        ]
        photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
        caption = await ai_client.text_request(request_message, prompt)
        await message.answer_photo(
            photo=photo_file,
            caption=caption,
            reply_markup=kb_start(),
        )
    await state.clear()


@ai_handler.message(CelebrityDialog.wait_for_answer)
async def ai_celebrity_answer(message: Message, state: FSMContext):
    user_text = 'Goodbye my love. Goodbye!' if message.text == 'Back' else message.text

    data = await state.get_data()
    user_request = {'role': 'user',
                    'content': user_text,
                    }
    data['dialog'].append(user_request)
    celebrity_response = await ai_client.text_request(data['dialog'], data['prompt'] + '.txt')
    celebrity_response_dict = {
        'role': 'assistant',
        'content': celebrity_response,
    }
    data['dialog'].append(celebrity_response_dict)
    await state.update_data(dialog=data['dialog'])
    await message.answer_photo(
        photo=FSInputFile(path=os.path.join('images', data['prompt'] + '.jpg')),
        caption=celebrity_response,
    )
    if message.text == 'Back':
        await state.clear()
        await com_start(message)


@ai_handler.callback_query(QuizData.filter(F.button == 'select_quiz'))
async def select_quiz(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    data = await state.get_data()

    data['score'] = data.get('score', 0)
    if callback_data.subject != 'quiz_more':
        data['type'] = callback_data.subject

    message_list = [
        {'role': 'user',
         'content': data['type']}
    ]

    ai_question = await ai_client.text_request(message_list, 'quiz.txt')
    photo_file = FSInputFile(path=os.path.join('images', 'quiz.jpg'))

    data['question'] = ai_question

    await state.update_data(data)

    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo_file,
        caption=ai_question,
    )
    await state.set_state(QuizGame.wait_for_answer)


@ai_handler.message(QuizGame.wait_for_answer)
async def quiz_correct_answer(message: Message, state: FSMContext):
    user_answer = message.text
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    data = await state.get_data()

    request_message = [
        {'role': 'assistant',
         'content': data['question']
         },
        {'role': 'user',
         'content': user_answer,
         },
    ]
    ai_answer = await ai_client.text_request(request_message, 'quiz.txt')
    photo_file = FSInputFile(path=os.path.join('images', 'quiz.jpg'))
    correct_answer = ai_answer.split(' ', 1)[0]
    if correct_answer == 'Correct':
        data['score'] += 1
        await state.update_data(score=data['score'])
    await message.answer_photo(
        photo=photo_file,
        caption=ai_answer + f'\nYour current score {data['score']}',
        reply_markup=ikb_next_quiz(),
    )
    await state.set_state(QuizGame.quiz_next_step)


@ai_handler.message(F.content_type == 'voice')
async def process_voice_message(message: Message):
    file_id = message.voice.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    file_name = f"files/audio{file_id}.mp3"
    await message.bot.download_file(file_path, file_name)

    audio = AudioSegment.from_file(file_name)
    wav_file = file_name.replace(".mp3", ".wav")
    audio.export(wav_file, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)

    request = recognizer.recognize_google(audio_data, language="ru-RU")
    prompt = 'Read it and respond to my request'

    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.RECORD_VOICE,
    )

    request_message = [
        {'role': 'user', 'content': request},
    ]

    caption = await ai_client.text_request(request_message, prompt)

    tts = gTTS(caption, lang='ru')
    audio_file_path = "files/response.mp3"
    tts.save(audio_file_path)

    audio_file = FSInputFile(path=audio_file_path)
    await message.answer_voice(voice=audio_file)

    os.remove(audio_file_path)


@ai_handler.message(Command('translator'))
async def translate_text(message: Message):
    content = message.text[len('/translator '):]

    if not content:
        await message.answer("Please provide text to translate.")
        return

    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )

    prompt = f'Translate the following text to English: "{content}"'
    request_message = [{'role': 'user', 'content': content}]

    caption = await ai_client.text_request(request_message, prompt)

    await message.answer(text=caption)
