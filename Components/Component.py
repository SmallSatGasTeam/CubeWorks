import asyncio

class Component:
    """
    An abstract class representing a framework component.  
    """
    def __init__(self, name, delay, initial_delay=0):
        """
        Initializes the Component object with a manditory name, delay and optional initial_delay.
        1. name is a string that identifies the component
        2. delay determines the frequency at which the component updates itself
        3. self.initial_delay is an optional parameter set to 0 by default.  This is used when the component shouldn't update immediately upon first run.
        """
        self.name = name
        self.delay = delay
        self.initial_delay = initial_delay

    def update(self, context):
        """
        An abstract method that defines the behavior of the component.
        Define this in child classes.
        """
        pass

    async def run(self, context, lock):
        """
        Controls the update cycle of the component.
        1. context is the mission mode defined in mission_modes file and passed to run() from main
        2. lock controls asynchronous execution so no race conditions occur
        run() waits for the self.initial_delay time to pass before beginning component updates
        """
        if self.initial_delay > 0:
            await asyncio.sleep(self.initial_delay)
            self.initial_delay = 0

        while True:
            async with lock:
                self.update(context)
            await asyncio.sleep(self.delay)
