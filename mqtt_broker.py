from hbmqtt.broker import Broker

config = {
    "listeners": {"default": {"type": "tcp", "bind": "0.0.0.0:1883"}},
    "sys_interval": 10,
    "topic-check": {"enabled": True}
}

broker = Broker(config)

async def start_broker():
    await broker.start()

import asyncio
asyncio.run(start_broker())
