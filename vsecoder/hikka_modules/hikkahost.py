# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the Copyleft license.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: hikkahost
# Author: vsecoder
# Commands:
# .hstart | .hstop | .hrestart | .hlogs | .h
# ---------------------------------------------------------------------------------

"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2022 t.me/vsecoder                                                            
    This program is free software; you can redistribute it and/or modify 

"""
# meta developer: @vsecoder_m
# meta pic: https://hikkahost.tech/logo.png
# meta banner: https://chojuu.vercel.app/api/banner?img=https://hikkahost.tech/logo.png&title=HikkahostMod&description=Hikkahost%20manager,%20buy%20hosting:%20@hikkahost_bot

__version__ = (4, 0, 0)

import asyncio
import logging
import os

from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)


@loader.tds
class HikkahostMod(loader.Module):
    """Hikkahost manager, buy hosting: @hikkahost_bot"""

    strings = {
        "name": "Hikkahost",
        "start": (
            "<emoji document_id=5172906452943110742>💻</emoji> <b>HikkaHost started</b>"
        ),
        "stop": (
            "<emoji document_id=5172915545388876587>💻</emoji> <b>HikkaHost stopped</b>"
        ),
        "restart": (
            "<emoji document_id=5172868665820840610>💻</emoji> <b>HikkaHost"
            " restarted</b>"
        ),
        "logs": (
            "<emoji document_id=5175188463556756015>💻</emoji> <b>HikkaHost"
            " logs:\n</b>{}"
        ),
        "loading": (
            "<emoji document_id=5841344801768738559>🔵</emoji> <b>In progress...</b>"
        ),
        "error": (
            "<emoji document_id=5843952899184398024>🚫</emoji> <b>Something went"
            " wrong</b>"
        ),
        "info": "<emoji document_id=5172441295100052110>💻</emoji> <b>Info:</b>",
        "not_hikkahost": (
            "<emoji document_id=5843952899184398024>🚫</emoji> <b>Not hikkahost, please"
            " buy hosting in @hikkahost_bot</b>"
        ),
    }

    strings_ru = {
        "start": (
            "<emoji document_id=5172906452943110742>💻</emoji> <b>HikkaHost запущен</b>"
        ),
        "stop": (
            "<emoji document_id=5172915545388876587>💻</emoji> <b>HikkaHost"
            " остановлен</b>"
        ),
        "restart": (
            "<emoji document_id=5172868665820840610>💻</emoji> <b>HikkaHost"
            " перезапущен</b>"
        ),
        "logs": (
            "<emoji document_id=5175188463556756015>💻</emoji> <b>HikkaHost"
            " логи:\n</b>{}"
        ),
        "loading": (
            "<emoji document_id=5841344801768738559>🔵</emoji> <b>В процессе...</b>"
        ),
        "error": (
            "<emoji document_id=5843952899184398024>🚫</emoji> <b>Что-то пошло не"
            " так</b>"
        ),
        "info": "<emoji document_id=5172441295100052110>💻</emoji> <b>Инфо:</b>",
        "not_hikkahost": (
            "<emoji document_id=5843952899184398024>🚫</emoji> <b>Not hikkahost, please"
            " buy hosting in @hikkahost_bot</b>"
        ),
    }

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.host = True

        if not "HIKKAHOST" in os.environ:
            self.host = False
            logger.error("Not hikkahost, please buy hosting")
            await self.inline.bot.send_message(
                self._tg_id, "Not hikkahost, please buy hosting"
            )

        self._client = client
        self.me = await client.get_me()
        self.bot = "@hikkahost_bot"

    async def get_response(self, command, timeout=10):
        async with self.client.conversation(self.bot, timeout=timeout) as conv:
            m = await conv.send_message(command)
            try:
                r = await conv.get_response()
            except asyncio.TimeoutError:
                return None
            await asyncio.sleep(timeout)
            await m.delete()
            await r.delete()

        return r

    async def hstartcmd(self, message):
        """
        - Start hikkahost
        """
        if not self.host:
            return await utils.answer(message, self.strings["not_hikkahost"])
        await utils.answer(message, self.strings["loading"])
        await self.get_response("/action start")
        await utils.answer(message, self.strings["start"])

    async def hstopcmd(self, message):
        """
        - Stop hikkahost
        """
        if not self.host:
            return await utils.answer(message, self.strings["not_hikkahost"])
        await utils.answer(message, self.strings["loading"])
        await self.get_response("/action stop")
        await utils.answer(message, self.strings["stop"])

    async def hrestartcmd(self, message):
        """
        - Restart hikkahost
        """
        if not self.host:
            return await utils.answer(message, self.strings["not_hikkahost"])
        await utils.answer(message, self.strings["loading"])
        await self.get_response("/action restart")
        await utils.answer(message, self.strings["restart"])

    async def hlogscmd(self, message):
        """
        - Get hikkahost logs
        """
        if not self.host:
            return await utils.answer(message, self.strings["not_hikkahost"])
        await utils.answer(message, self.strings["loading"])
        r = await self.get_response("/action logs", 3)
        if not r or not r.message:
            return await utils.answer(message, self.strings["error"])
        await utils.answer(message, self.strings["logs"].format(r.message))

    async def hcmd(self, message):
        """
        - Get hikkahost info
        """
        query = await message.client.inline_query(self.bot, " ")
        if not query:
            return await utils.answer(message, self.strings["error"])

        await utils.answer(message, self.strings["info"])
        await query[0].click(utils.get_chat_id(message), message.reply_to_msg_id)
