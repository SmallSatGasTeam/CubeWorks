import asyncio

class Driver:
    def __init__(self, name, delay=1, initial_delay=0):
        self.name = name
        self.delay = delay
        self.initial_delay = initial_delay

    def read(self):
        pass

    async def run(self, context, lock):
        if self.initial_delay > 0:
            await asyncio.sleep(self.initial_delay)
            self.initial_delay = 0

        while True:
            reading = self.read()
            async with lock:
                context[self.name] = reading
            await asyncio.sleep(self.delay)
