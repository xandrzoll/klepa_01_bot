import logging
import ssl
import sys

from aiohttp import web

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from settings import (
    TG_BOT, WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV, WEBHOOK_PATH,
    WEBHOOK_SECRET, BASE_WEBHOOK_URL
)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8080

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker etc.)
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        certificate=FSInputFile(WEBHOOK_SSL_CERT),
        secret_token=WEBHOOK_SECRET,
    )

async def index(request):
    logging.info(request)
    return web.Response(text="Welcome home!")

async def print_message(request):
    logging.info(request)
    data = {'some': 'data'}
    return web.json_response(data)


async def main() -> web.Application:
    dp = Dispatcher()

    dp.include_router(router)

    dp.startup.register(on_startup)

    bot = Bot(TG_BOT, parse_mode=ParseMode.HTML)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    app.router.add_get('/', index)
    app.router.add_get('/my_super_message123321', print_message)
    return app
