import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

from config import ADMIN_ID
from clients import bot_client, user_client

from function.users.user_command import is_spamming_now, get_total_send

#######################
def is_admin(user_id: int):
    return user_id in ADMIN_ID
#######################

@bot_client.on_message(filters.command(commands='start'))
async def cmd_start(client: Client, message: Message):
    text = (
        f'<b>🙋 Добро пожаловать в лучшего бота для рассылки - SpamTalent</b>\n\n'
        f'<i>Бот создан при поддержке @deartalent | Dev: @conorxz</i>'
    )
    await message.delete()
    await message.reply(text=text)

@bot_client.on_message(filters.command(["status", "stats", "статус", "стат"]))
async def cmd_status(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        return
    
    total_send = get_total_send()
    status_text = "🟢 <b>Активна</b>" if is_spamming_now() else "🔴 <b>Остановлена</b>"
    text = (
        f"<b>📊 Статус бота:</b>\n\n"
        f'{status_text}\n'
        f'<b>📨 Отправленно:</b> {total_send}'
    )

    msg = await message.reply(text=text)
    await asyncio.sleep(30)
    msg.delete()