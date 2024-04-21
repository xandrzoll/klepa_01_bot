from aiogram import Bot
from aiogram.enums import ParseMode
from aiohttp import web
from pydantic import BaseModel, ValidationError
from typing import List

from settings import SECRET_VALUE, TG_BOT
from src.webapp.routes.base import require_headers

class MessageData(BaseModel):
    message: str
    chat: List[int]

class RequestData(BaseModel):
    data: List[MessageData]


bot = Bot(TG_BOT, parse_mode=ParseMode.HTML)
routes = web.RouteTableDef()

@routes.post('/post_message')
@require_headers({'Content-Type': 'application/json', 'X-Secret-Value': SECRET_VALUE})
async def send_tg_message(request: web.Request):
    if request.body_exists:
        data = await request.json()
        try:
            messages = RequestData(**data)
        except ValidationError as e:
            return web.json_response({"error": f"Ошибка валидации: {e}"})
        for message in messages.data:
            for chat in message.chat:
                await bot.send_message(chat_id=chat, text=message.message)
    return web.json_response({"data": "ok!"})
