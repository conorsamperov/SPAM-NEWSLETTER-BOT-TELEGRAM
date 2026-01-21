import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

from config import ADMIN_ID
from clients import user_client
from chat_id import get_chats

saved_message = None
is_spamming = False
current_spam_task = None
total_send = 0

#######################
def get_saved_message():
    return saved_message

def has_saved_message():
    return saved_message is not None

def start_spam():
    global total_send
    global is_spamming
    is_spamming = True
    total_send = 0

def stop_spam():
    global total_send
    global is_spamming
    is_spamming = False
    total_send = 0

def is_spamming_now():
    return is_spamming

def get_total_send():
    global total_send
    return total_send

def is_admin(user_id: int):
    return user_id in ADMIN_ID
#######################
@user_client.on_message(filters.command(["сохранить", "сохр", "save", 'сейв'], prefixes="."))
async def cmd_save(client: Client, message: Message):
    global saved_message

    await message.delete()
    waiting = await message.reply("<b>💭 Обрабатываю..</b>")
    await asyncio.sleep(4)
    if not message.reply_to_message:
        delete_msg = await waiting.edit("<b>📩 Ответьте на сообщение, которое хотите сохранить!</b>")
        await asyncio.sleep(25)
        await delete_msg.delete()
        return
    
    saved_message = {
        "chat_id": message.reply_to_message.chat.id,
        "message_id": message.reply_to_message.id,
    }
    await waiting.edit(f"<b>✅ Текст успешно сохранён</b>")
    await asyncio.sleep(10)
    await waiting.delete()

@user_client.on_message(filters.command(["удалить", "уд", "clear"], prefixes="."))
async def cmd_clear(client: Client, message: Message):
    global saved_message

    await message.delete()
    waiting = await message.reply("<b>💭 Обрабатываю..</b>")
    await asyncio.sleep(3)
    
    saved_message = None
    await waiting.edit("<b>🗑️ Сообщение успешно удалено из памяти!</b>")
    await asyncio.sleep(60)
    await waiting.delete()

@user_client.on_message(filters.command(["тест", "test", "тт"], prefixes='.'))
async def cmd_test(client: Client, message: Message):
    await message.delete()
    waiting = await message.reply("<b>💭 Обрабатываю..</b>")
    await asyncio.sleep(8)
    if not has_saved_message():
        await waiting.edit("<b>❌ У вас нет сохранённого сообщения!")
        return
    
    msg_data = get_saved_message()

    await waiting.delete()
    await client.forward_messages(
        chat_id=message.chat.id,
        from_chat_id=msg_data["chat_id"],
        message_ids=msg_data["message_id"]
    )

###################################################################

async def spam_messages(client, msg_data, delay_seconds=20):
    chats = get_chats()
    
    print(f"🚀 Рассылка начата в {len(chats)} чатов")
    
    while is_spamming_now():
        for chat_id in chats:
            if not is_spamming_now():
                print("🛑 Остановка внутри цикла")
                return
            
            try:
                print(f"📤 Отправляю в {chat_id}")

                global total_send
                total_send += 1

                await client.forward_messages(
                    chat_id=chat_id,
                    from_chat_id=msg_data["chat_id"],
                    message_ids=msg_data["message_id"]
                )
                print(f"✅ Отправлено в {chat_id}")
                
            except Exception as e:
                print(f"❌ Ошибка в {chat_id}: {e}")
            
            print(f"⏳ Жду {delay_seconds} секунд...")
            for i in range(delay_seconds):
                if not is_spamming_now():
                    print("🛑 Остановка во время ожидания")
                    return
                await asyncio.sleep(1)
        
        if is_spamming_now():
            print("🔄 Начинаю новый круг рассылки...")
    
    print("🛑 Рассылка завершена")

@user_client.on_message(filters.command(["старт", "send", "флуд"], prefixes='.'))
async def cmd_send(client: Client, message: Message, delay_seconds=20):
    await message.delete()
    
    if is_spamming_now():
        msg = await message.reply("<b>⚠️ Рассылка уже запущена!</b>")
        await asyncio.sleep(3)
        await msg.delete()
        return
    
    if not has_saved_message():
        msg = await message.reply("<b>❌ У вас нет сохранённого сообщения!</b>")
        await asyncio.sleep(3)
        await msg.delete()
        return
    
    waiting = await message.reply("<b>🚀 Запускаю рассылку...</b>")
    await asyncio.sleep(3)
    
    start_spam()
    
    msg_data = get_saved_message()
    chats = get_chats()
    
    await waiting.edit(f"<b>✅ Рассылка начата в {len(chats)} чатов!</b>\n\n<b>Интервал:</b> 20 секунд\n<b>Для остановки:</b> .стоп")
    await asyncio.sleep(10)
    await waiting.delete()
    
    asyncio.create_task(spam_messages(client, msg_data))

@user_client.on_message(filters.command(["стоп", "stop", "стфлуд", "ст"], prefixes="."))
async def cmd_stop(client: Client, message: Message):
    await message.delete()
    
    if not is_spamming_now():
        msg = await message.reply("<b>⚠️ Рассылка не запущена!</b>")
        await asyncio.sleep(3)
        await msg.delete()
        return
    
    waiting = await message.reply("<b>🛑 Останавливаю рассылку...</b>")
    await asyncio.sleep(2)
    
    # Останавливаем
    stop_spam()
    
    await waiting.edit("✅ Рассылка успешно остановлена!")
    await asyncio.sleep(3)
    await waiting.delete()

@user_client.on_message(filters.command("id", prefixes="."))
async def get_my_group_id(client: Client, message: Message):
    await message.delete()
    if message.chat.type == "private":
        await message.reply("❌ Эта команда работает только в группах!")
        return
    
    chat_id = message.chat.id
    text = (
        f"<b>📌 ID этой группы:</b>\n\n"
        f"<code>{chat_id}</code>\n\n"
        f"<b>Тип чата:</b> {message.chat.type}\n"
        f"<b>Скопируй этот ID в chat_id.py</b>"
    )
    await message.reply(chat_id='me', text=text)