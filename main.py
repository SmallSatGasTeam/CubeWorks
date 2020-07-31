import asyncio
from datetime import datetime
from time import sleep

from Components import *
from Drivers import *
from mission_modes import *
from mission_logic import *

async def startLoop(db):
    """
    Creates a context dictionary to contain values,
    Creates a lock to prevent race conditions when running drivers,
    Initializes all drivers in a list,
    Starts gathering from Driver.run() on loop
    """
    context = {"MissionMode": MissionMode.PRE_TX}
    lock = asyncio.Lock()
    drivers = [ContextPrinter(), RTC(), db]
    await asyncio.gather(*[d.run(context, lock) for d in drivers], runLogic(drivers, context, lock))


def UTCTime():
    """
    Returns the UTC time in miliseconds since the Unix epoch.
    The integer returned should be 64 bits in size and be on the order of 1500000000000.
    """
    return int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)


if __name__ == '__main__':
    """
    The main entry point for CubeWorks.  Performs the following tasks:
    1. Sets the sleep duration before beginning operations
    2. Initializes the database
    3. Computes the time to wait before beginning operations in case of reboot
    4. Waits if the sleep duration has not elapsed
    5. Begins the main asyncio loop
    """
    # Time in miliseconds to sleep before initializing drivers
    SLEEP_DURATION = 10 * 1000#30 * 60

    # Initialilze database
    db = Database()

    # Query database for initial time
    initial_time = db.getFirstBoot()

    if initial_time is None:
        # Record initial boot time in database
        print('initial time not found: assuming first boot')
        initial_time = UTCTime()
        db.setFirstBoot(initial_time)

    delta = UTCTime() - initial_time
    if delta < SLEEP_DURATION:
        print(f'wait time not elapsed.  waiting {delta}')
        sleep((SLEEP_DURATION - delta) / 1000)

    try:
        asyncio.run(startLoop(db))
    except KeyboardInterrupt:
        pass
