import asyncio

async def runLogic(drivers, context, lock):
    """
    Uses the context dictionary to determine what to do with the sattelite.
    The driver objects are passed in from main to access the command methods for the hardware.
    Lock is used to prevent other coroutines from accessing a resource while this coroutine is.  
    """
    delay = 1 # This delay should be determined by the mission mode in context
    while True:
        print("running logic") # this line is a stand in.  remove later.
        ###########################
        # Perform logic checks here
        #||||||||||||||||||||||||||
        #VVVVVVVVVVVVVVVVVVVVVVVVVV
        
        # No logic past this point
        await asyncio.sleep(delay)
