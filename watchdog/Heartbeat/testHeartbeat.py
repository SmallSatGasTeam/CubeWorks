import Heartbeat
import asyncio

""" Tests if heartbeat is working """

Heartbeat.setUp()
asyncio.run(Heartbeat.longTap())
