# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: spf
# Author: AlpacaGang
# Commands:
# .spf
# ---------------------------------------------------------------------------------

# fuck python the encoding: utf-8
import asyncio
import datetime
import logging
import time

from .. import loader, utils

logger = logging.getLogger(__name__)


def register(cb):
    cb(SPFMod())


@loader.tds
class SPFMod(loader.Module):
    """Этот модуль геи личку ваших друзей"""

    strings = {"name": "ЖУЖАКА НАХУЙ"}

    def __init__(self):
        self.name = self.strings["name"]

    def config_complete(self):
        pass

    async def spfcmd(self, message):
        """Чтобы использовать пишем так: .spf @ник_вашего_друга"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(
                message,
                (
                    "Вы не указали кому хотите писать\nЧтобы использовать напишите так:"
                    " .spf @ник_вашего_друга"
                ),
            )
            return
        who = args[0][1:]
        conv = message.client.conversation("t.me/" + who, timeout=5, exclusive=True)
        for i in range(100):
            await conv.send_message("Ты гей")
