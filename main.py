from zabbix_utils import ZabbixAPI
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "env_tokens/tokens.env"
load_dotenv(dotenv_path=env_path)

DOMAIN = os.getenv("ZABBIX_URL")

api = ZabbixAPI(url=DOMAIN)
api.login(user="Admin", password="zabbix")

hosts = api.host.get(
    filter={
        "host": [
            "Zabbix server",
            "Linux server"
        ]
    }
)

hostid = hosts[0]["hostid"]

cpu_items = api.item.get(
    hostids=hosts[0]["hostid"],
    search={"key_": "system.cpu.load"},  # ищем метрики загрузки CPU
    output=["itemid", "name", "key_", "lastvalue", "lastclock", "value_type"]
)

uptime_items = api.item.get(
    hostids=hosts[0]["hostid"],
    search={"key_": "system.uptime"},  # ищем метрики загрузки CPU
    output=["lastvalue", "lastclock", "prevvalue", "units", "value_type", "state", "error"]
)

memory_items = api.item.get(
    hostids=hosts[0]["hostid"],
    search={"key_": "vm.memory.size[available]"},  # ищем метрики загрузки CPU
    output=["lastvalue", "units", "value_type", "lastclock"]
)

# for item in memory_items:
#     print(item["lastvalue"])
#     print(item["units"])
#     print(item["value_type"])
#     print(item["lastclock"])

# for item in uptime_items:
#     print(item["lastvalue"])
#     print(item["lastclock"])
#     print(item["prevvalue"])
#     print(item["units"])
#     print(item["value_type"])
#     print(item["state"])
#     print(item["error"])

# for item in cpu_items:
#     print(item["itemid"])
#     print(item["name"])
#     print(item["lastvalue"])
#     print(item["lastclock"])
#     print(item["value_type"])

# users = api.user.get(
#     output=['userid','name']
# )

# for host in hosts:
#     print(host)

# for user in users:
#     print(user['name'])

api.logout()
