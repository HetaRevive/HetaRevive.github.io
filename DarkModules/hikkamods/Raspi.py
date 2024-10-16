# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: Raspi
# Author: DarkModules
# Commands:
# .rinfo | .shutdown | .reboot
# ---------------------------------------------------------------------------------

# The MIT License (MIT)
# Copyright (c) 2022 penggrin

# meta developer: @penggrinmods
# requires: psutil distro
# scope: hikka_only

import logging
import subprocess
import time

import distro
import psutil

from .. import loader, utils

logger = logging.getLogger(__name__)


def b2m(b: int) -> int:
    return round(b / 1024 / 1024, 1)


@loader.tds
class RaspiMod(loader.Module):
    """Control ya Raspberry Pi remotely"""

    strings = {
        "name": "Raspi",
        "info": (
            "\n🌡 CPU Temperature: `{}`"
            "⚡️ Voltage: `{}`"
            "🔼 Uptime: `{}`"
            "\n"
            "🖥 CPU: `{}` Cores (`{}%`)\n"
            "💽 RAM: `{}` MB / `{}` MB (`{}%`)\n"
            "💾 Disk: `{}` MB / `{}` MB (`{}%`)"
        ),
        "shutting": "🔄 Shutting down!\n🔄 Bye!!!",
        "rebooting": "🔄 Rebooting...",
        "rebooted": "✅ Done Rebooting! ({}s)",
        "started": "💫 <b>{}</b> Started!",
        "low_voltage": "⚠️ Low Voltage Detected!\n",
        "high_temp": "⚠️ High CPU Temperature Detected!\n",
        "low_voltage_threshold_config": "Low Voltage Warning Threshold",
        "high_temperature_threshold_config": "High Temperature Warning Threshold",
    }

    strings_ru = {
        "info": (
            "\n🌡 Температура CPU: `{}`"
            "⚡️ Напряжение: `{}`"
            "🔼 Время работы: `{}`"
            "\n"
            "🖥 CPU: `{}` Ядер (`{}%`)\n"
            "💽 ОЗУ: `{}` МБ / `{}` МБ (`{}%`)\n"
            "💾 Диск: `{}` МБ / `{}` МБ (`{}%`)"
        ),
        "shutting": "🔄 Выключаюсь!\n🔄 Пока!!!",
        "rebooting": "🔄 Перезапускаюсь...",
        "rebooted": "✅ Успешно перезапустился! ({}с)",
        "started": "💫 <b>{}</b> Запущен!",
        "low_voltage": "⚠️ Замечено низкое напряжение!\n",
        "high_temp": "⚠️ Замечена высокая температура CPU!\n",
        "low_voltage_threshold_config": "Порог предупреждения о низком напряжении",
        "high_temperature_threshold_config": (
            "Порог предупреждения о высокой температуре"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "low_voltage_threshold",
                4.9,
                doc=lambda: self.strings("low_voltage_threshold_config"),
                validator=loader.validators.Float(),
            ),
            loader.ConfigValue(
                "high_temp_threshold",
                60,
                doc=lambda: self.strings("high_temperature_threshold_config"),
                validator=loader.validators.Integer(),
            ),
        )

    async def client_ready(self):
        if not self.get("rebooting"):
            await self._client.send_message(
                "me", self.strings("started").format(distro.name(pretty=True))
            )
            return

        logger.debug("Done rebooting!")

        chat_id, message_id = self.get("rebooting").split(":")
        chat_id, message_id = int(chat_id), int(message_id)
        time_passed = int(time.time() - self.get("reboot_time"))
        await self._client.edit_message(
            chat_id, message_id, self.strings("rebooted").format(time_passed)
        )

        self.set("rebooting", None)

    @loader.command(ru_doc="Получить немного информации о твоей Raspberry Pi")
    async def rinfocmd(self, message):
        """Get some information about ur Raspberry Pi"""
        temp = (
            subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        ).split("=")[1]
        voltage = (
            subprocess.check_output(["vcgencmd", "measure_volts"]).decode("utf-8")
        ).split("=")[1]
        uptime = (subprocess.check_output(["uptime", "-p"]).decode("utf-8")).split(
            "up "
        )[1]
        cores = psutil.cpu_count(logical=True)
        cpu = psutil.cpu_percent()
        ram = b2m(psutil.virtual_memory().total - psutil.virtual_memory().available)
        ram_total = b2m(psutil.virtual_memory().total)
        ram_perc = psutil.virtual_memory().percent
        hdd = psutil.disk_usage("/")

        await utils.answer(
            message,
            f"🍇 **{distro.name(pretty=True)}**\n\n"
            + (
                self.strings("low_voltage")
                if float(voltage.split("V")[0]) < self.config["low_voltage_threshold"]
                else ""
            )
            + (
                self.strings("high_temp")
                if float(temp.split("'C")[0]) > self.config["high_temp_threshold"]
                else ""
            )
            + self.strings("info").format(
                temp,
                voltage,
                uptime,
                cores,
                cpu,
                ram,
                ram_total,
                ram_perc,
                b2m(hdd.used),
                b2m(hdd.total),
                hdd.percent,
            ),
            parse_mode="Markdown",
        )

    @loader.command(ru_doc="Выключить Raspberry Pi")
    async def shutdowncmd(self, message):
        """Shutdown Raspberry Pi"""
        await utils.answer(message, self.strings("shutting"))
        subprocess.run(["sudo", "shutdown", "now"])

    @loader.command(ru_doc="Перезапустить Raspberry Pi")
    async def rebootcmd(self, message):
        """Reboot Raspberry Pi"""
        msg = await utils.answer(message, self.strings("rebooting"))
        self.set("rebooting", f"{utils.get_chat_id(msg)}:{msg.id}")
        self.set("reboot_time", time.time())
        subprocess.run(["sudo", "reboot"])
