import asyncio


class Driver:
    def __init__(self, name, delay):
        self.delay = delay
        self.name = name

    def read(self):
        pass

    async def run(self, context, lock):
        while True:
            reading = self.update()
            async with lock:
                context[self.name] = reading
            await asyncio.sleep(self.delay)