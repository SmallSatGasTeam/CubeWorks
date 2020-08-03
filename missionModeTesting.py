import asyncio
from flightLogic import saveTofiles
from flightLogic.missionModes import preBoomDeploy
from flightLogic.missionModes import antennaDeploy
from flightLogic.missionModes import boomDeploy
from flightLogic.missionModes import postBoomDeploy

def testPreBoomDeploy():
	saveObject = saveTofiles.save()
	missionMode = preBoomDeploy.preBoomMode(saveObject)
	asyncio.run(missionMode.run())

def testAntennaDeploy():
	saveObject = saveTofiles.save()
	missionMode = antennaDeploy.antennaMode(saveObject)
	asyncio.run(missionMode.run())

# presten: these following methods were both named testPreBoomDeploy so i fixed the names
def testBoomDeploy():
	saveObject = saveTofiles.save()
	missionMode = boomDeploy.boomMode(saveObject)
	asyncio.run(missionMode.run())

def testPostBoomDeploy():
	saveObject = saveTofiles.save()
	missionMode = postBoomDeploy.postBoomMode(saveObject)
	asyncio.run(missionMode.run())
