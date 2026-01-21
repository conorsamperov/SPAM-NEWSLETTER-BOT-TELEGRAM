"""
╔══════════════════════════════════════╗
║                                      ║
║        🚀 SPAM | TALENT TEAM 🚀     ║
║       При поддержке: @deartalent     ║
║       Автор: CONOR                   ║
║       Версия: 0.1                    ║
║                                      ║
╚══════════════════════════════════════╝
"""

import asyncio
import logging
from pyrogram import idle
from clients import bot_client, user_client

from pyrogram import Client

app = Client("my_account")

#########################
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.dispatcher").setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s',
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
#########################

async def main():
    await asyncio.gather(
        bot_client.start(),
        user_client.start()
    )
    try:
        import function.bot.command
        import function.users.user_command
        logger.info("HANDLERS START!")
    except Exception as e:
        logger.error("Error in starting (HANDLERS)")
    await idle()

if __name__ == "__main__":
    bot_client.loop.run_until_complete(main())
    logger.info("SPAMER START!")