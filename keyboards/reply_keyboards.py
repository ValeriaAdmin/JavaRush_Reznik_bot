from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_start():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Random fact',
    )
    keyboard.button(
        text='GPT chat request',
    )
    keyboard.button(
        text='Dialog with person',
    )
    keyboard.button(
        text='Quiz',
    )
    keyboard.button(
        text='Help',
    )
    keyboard.adjust(2, 2, 1)

    return keyboard.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Select a menu item..'
    )


def kb_random_facts():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='I want another fact'
    )
    keyboard.button(
        text='Finish'
    )
    return keyboard.as_markup(
        resize_keyboard=True,
    )


def kb_back():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Back'
    )
    return keyboard.as_markup(
        resize_keyboard=True,
    )
