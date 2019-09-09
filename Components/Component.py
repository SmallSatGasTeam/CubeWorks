import asyncio


class Component:
    def __init__(self, name, delay):
        self.delay = delay
        self.name = name

    def update(self, context):
        pass

    async def run(self, context, lock):
        while True:
            async with lock:
                self.update(context)
            await asyncio.sleep(self.delay)
