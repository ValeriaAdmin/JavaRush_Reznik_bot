# ChatGPT Telegram Bot

This bot is designed for interacting with **ChatGPT** and includes various features such as sending random facts, responding to queries, simulating conversations with famous personalities, playing a QUIZ game, as well as supporting voice messages and translating text from Russian to English.

## Features

- **ChatGPT Queries**: You can send any text queries, and the bot will respond using ChatGPT.
- **Random Facts**: The bot can send a random interesting fact upon request.
- **Simulating Conversations with Famous Personalities**: The bot can imitate dialogues with famous personalities, providing responses in their style.
- **QUIZ**: The bot can conduct a quiz with questions and scores.
- **Voice Messages**: The bot supports sending and receiving voice messages.
- **Text Translation**: The bot can translate text from Russian to English upon request.

## Installation

To start working with this project, follow these steps:

### Cloning the Repository

```bash
git clone https://github.com/ValeriaAdmin/JavaRush_Reznik_bot.git
```

### Installing Dependencies

```bash
cd JavaRush_Reznik_bot
pip install -r requirements.txt
```

## Usage

1. Copy your bot token from **BotFather**.
2. Create a `config.py` file and add your bot token:

```python
API_TOKEN = 'YOUR_BOT_API_TOKEN'
```

3. Run the project:

```bash
python bot.py
```

4. The bot will be ready to work, and you can start interacting with it on Telegram.

## Commands

- `/start` - Start interacting with the bot.
- `/random` - Get a random fact.
- `/gpt` - Start a conversation with ChatGPT.
- `/quiz` - Play a quiz game.
- `/talk` - Have a conversation with a famous personality.
- `/translator <text>` - Translate text from Russian to English.

## Usage Example

- **ChatGPT Queries**: Simply send a text message, and the bot will respond using ChatGPT.
- **Random Facts**: Send the `/random` command, and the bot will send you a random interesting fact.
- **Simulating Conversations with Famous Personalities**: Type `/talk <name>`, and the bot will start imitating a dialogue with the personality of your choice.
- **QUIZ**: Send the `/quiz` command, and the bot will start a quiz with questions.
- **Voice Messages**: You can send voice messages, and the bot will respond to them.
- **Text Translation**: Type `/translate <text in Russian>`, and the bot will translate the text into English.

## Contact

If you have any questions or suggestions, you can contact me via email:

📧 **Email**: reznik9711@gmail.com

