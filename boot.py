from datetime import datetime
from time import sleep

# Time in seconds to sleep before initializing drivers
SLEEP_DURATION = 30 * 60

# TODO: Query database for initial time
initial_time = None

if initial_time is None:
    initial_time = datetime.now()
    # TODO: Record initial boot time in database

delta = initial_time - datetime.now()
if delta.seconds < SLEEP_DURATION:
    sleep(SLEEP_DURATION - delta.seconds)
