import Heartbeat
import asyncio

Heartbeat.setUp()
asyncio.run(Heartbeat.longTap())
