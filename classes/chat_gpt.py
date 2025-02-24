import os
from enum import Enum

from openai import AsyncOpenAI


class GPTModel(Enum):
    TEXT_GPT = 'gpt-4o-mini'


class ChatGPT:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self._ai_token = os.getenv('TOKEN_API_PROXY')
        self._base_url = os.getenv('BASE_URL')
        self._client = self._create_client()

    def _create_client(self):
        ai_client = AsyncOpenAI(
            base_url=self._base_url,
            api_key=self._ai_token
        )
        return ai_client

    async def text_request(self, messages: list[dict[str, str]], prompt: str):
        message_list = [
                           {'role': 'system',
                            'content': prompt},
                       ] + messages
        completion = await self._client.chat.completions.create(
            messages=message_list,
            model='gpt-3.5-turbo'
        )
        response = completion.choices[0].message.content
        return response
