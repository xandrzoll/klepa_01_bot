from pathlib import Path
from environs import Env

ROOT_PATH = Path(__file__).parent.parent.resolve()
ENV_PATH = str(ROOT_PATH / 'settings' / '.env')

env = Env()
env.read_env(ENV_PATH)
TINKOFF_TOKEN = env.str('TINKOFF_TOKEN')
# TINKOFF_TOKEN_TRADE = env.str('TINKOFF_TOKEN_TRADE')
# TINKOFF_TRADE_ACCOUNT = env.str('TINKOFF_TRADE_ACCOUNT')
TINKOFF_WATCH_ACCOUNT = env.list('TINKOFF_WATCH_ACCOUNT', subcast=str)
# TINKOFF_COPY_ACCOUNT = env.list('TINKOFF_COPY_ACCOUNT', subcast=str)
TG_BOT = env.str('TG_BOT')
# TG_CHAT_IDS = env.list('TG_CHAT_IDS', subcast=int)
#
# DB_HOST = env.str('DB_HOST')
# DB_BASE = env.str('DB_BASE')
# DB_USER = env.str('DB_USER')
# DB_PASSWORD = env.str('DB_PASSWORD')

WEBHOOK_SSL_CERT = env.str('WEBHOOK_SSL_CERT')
WEBHOOK_SSL_PRIV = env.str('WEBHOOK_SSL_PRIV')
WEBHOOK_PATH = env.str('WEBHOOK_SSL_PRIV')
WEBHOOK_SECRET = env.str('WEBHOOK_SSL_PRIV')
BASE_WEBHOOK_URL = env.str('WEBHOOK_SSL_PRIV')