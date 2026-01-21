from pyrogram import Client
from pyrogram.enums import ParseMode
from config import API_HASH, API_ID, BOT_TOKEN

user_client = Client(name='USER_SESSION', api_id=API_ID, api_hash=API_HASH, parse_mode=ParseMode.HTML)
bot_client = Client(name='BOT_SESSION', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, parse_mode=ParseMode.HTML)