import asyncio

class Component:
    def __init__(self, name, delay, initial_delay=0):
        self.name = name
        self.delay = delay
        self.initial_delay = initial_delay

    def update(self, context):
        pass

    async def run(self, context, lock):
        if self.initial_delay > 0:
            await asyncio.sleep(self.initial_delay)
            self.initial_delay = 0

        while True:
            async with lock:
                self.update(context)
            await asyncio.sleep(self.delay)
