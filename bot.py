from typing import Self

from zabbix_utils import ZabbixAPI
from telebot import TeleBot
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "env_tokens/tokens.env"
load_dotenv(dotenv_path=env_path)

TG_TOKEN = os.getenv("TG_BOT_TOKEN")
ZABBIX_URL = os.getenv("ZABBIX_URL")
USER_NAME = os.getenv("ZABBIX_USER")
PASSWORD = os.getenv("ZABBIX_PASSWORD")
all_commands: list[str] = ["get_cpu", "get_memory", "get_uptime"]

api = ZabbixAPI(url=ZABBIX_URL)

def get_zabbix_metrics(name: str) -> dict:
    if name == "get_cpu" or name == "get_memory" or name == "get_uptime":
        api.login(user=USER_NAME, password=PASSWORD)
        hosts = api.host.get(
            filter={
                "host": [
                    "Zabbix server",
                    "Linux server"
                ]
            }
        )
        hostid = hosts[0]["hostid"]

        if name == "get_cpu":
            cpu_items = api.item.get(
                hostids=hosts[0]["hostid"],
                filter={"key_": "system.cpu.util"},
                output=["itemid", "name", "key_", "lastvalue", "lastclock", "units"]
            )
            api.logout()

            return cpu_items
        elif name == "get_memory":
            memory_items = api.item.get(
                hostids=hosts[0]["hostid"],
                filter={"key_": "vm.memory.size[available]"},
                output=["key_", "lastvalue", "units", "value_type", "lastclock"]
            )
            api.logout()

            return memory_items

        elif name == "get_uptime":
            uptime_items = api.item.get(
                hostids=hosts[0]["hostid"],
                filter={"key_": "system.uptime"},
                output=["key_", "lastvalue", "lastclock", "prevvalue", "units", "value_type", "state", "error"]
            )
            api.logout()

            return uptime_items


def get_baked_zabbix_metrics(metric_name: str) -> str:
    raw_metrics = get_zabbix_metrics(metric_name)
    print_text = None

    if metric_name == "get_cpu":
        print_text = "(Нагрузка процессора)"

    elif metric_name == "get_memory":
        print_text = "(Свободная память)"

    elif metric_name == "get_uptime":
        print_text = "(Время работы)"


    for item in raw_metrics:
        key = item["key_"]
        value = item["lastvalue"]
        units = item["units"]
        print(f"Метрика: {key} {print_text} | Значение: {value} {units}")

    return key, value, units


# get_baked_zabbix_metrics("get_cpu")
# get_baked_zabbix_metrics("get_memory")
# get_baked_zabbix_metrics("get_uptime")


bot = TeleBot(TG_TOKEN)

@bot.message_handler(commands=["start"])    #Стартовое сообщение для тг
def send_welcome(message):
    bot.send_message(message.chat.id, "Выберите тип данных для получения:")
    bot.reply_to(message, text=f" Команды для выбора {all_commands["get_cpu"]}, {all_commands["get_memory"]}, {all_commands["get_m"]}

@bot.message_handler(command=[all_commands])   #Метрики на вывод в тг
def tg_write_metric(message):
    bot.reply_to(message, all_commands)

bot.infinity_polling()