from zabbix_utils import ZabbixAPI
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "env_tokens/tokens.env"
load_dotenv(dotenv_path=env_path)

DOMAIN = os.getenv("ZABBIX_URL")
USER = os.getenv("ZABBIX_USER")
PASSWORD = os.getenv("ZABBIX_PASSWORD")

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
    filter={"key_": "system.cpu.util"},
    output=["itemid", "name", "key_", "lastvalue", "lastclock", "units"]
)

uptime_items = api.item.get(
    hostids=hosts[0]["hostid"],
    filter={"key_": "system.uptime"},
    output=["key_", "lastvalue", "lastclock", "prevvalue", "units", "value_type", "state", "error"]
)

memory_items = api.item.get(
    hostids=hosts[0]["hostid"],
    filter={"key_": "vm.memory.size[available]"},
    output=["key_", "lastvalue", "units", "value_type", "lastclock"]
)


for item in cpu_items:
    key = item["key_"]
    value = item["lastvalue"]
    units = item["units"]
    print(f"Метрика: {key} | Значение: {value} {units}")

for item in uptime_items:
    key = item["key_"]
    value = item["lastvalue"]
    units = item["units"]
    print(f"Метрика: {key} | Значение: {value} {units}")

for item in memory_items:
    key = item["key_"]
    value = item["lastvalue"]
    units = item["units"]
    print(f"Метрика: {key} | Значение: {value} {units}")

# users = api.user.get(
#     output=['userid','name']
# )

# for host in hosts:
#     print(host)

# for user in users:
#     print(user['name'])

api.logout()