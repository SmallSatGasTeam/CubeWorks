Psuedocode for Flight Logic
--
STARTING NOTES:

NOTE: drivers running at different hz must be done inside drivers depending on mission mode.

MAIN
--
This file will control running all the mission mode files. 
kinda like a parent or a guardian.

    runLogic(drivers, context, lock #Note:entry conditions):
        CheckSafe(): 
            If power < CritPower
                Go into safe mode
        
	checkBootMode():
		If antenna deployed == True:
			Resume = Get most recent datapoint from db
			Mission mode = resume
		Else:
			Wait for 30 + x minutes
			If antenna deployed == false:
				Deploy antenna
				Mission mode = ANTENNA DEPLOY
			Else:
				Mission mode = PRE-BOOM DEPLOY
				
		
	
SAFE
--
This mission mode will put the satellite into what is basically
low power mode.

	Send flag to watchdog telling Pi to power off

NOTE: Watchdog needs to handle exit conditions for SAFE

Antenna Deploy 
-- 
This mission mode will be run as many times as it takes to
 deploy the antenna. If needs be it will go to safe. this will work 
 very closely with the antennaDoor Driver. 

    antennaDeploy:
        NOTE: steps 2,3 and 4 from flight logic doc are in the antenna deploy driver.
        checkPower():
            While time elapsed < TimeOut:
             If eps value in context > CritPower 
                deployment():
                Antenna.deployed = true;
                Break out of loop
            Else:
                wait(1 min)
        If time elapsed > TimeOut:
            Go to SAFE
		
        deployment():
            Call antenna deploy driver
            
	
    boomDeploy():
        If boomDeploy conditions met:
            deployment():
                Call boom deploy driver
            takePicture()
            Boom.deployed = true;
            Mission mode = POST-BOOM DEPLOY

NOTE: post boom deploy step 2?

Transmission mode
--
This file will set up a communication line with the ground
 and will work call the code under the TXISR file. 

    transmission:
        evalPower():
            If tx window imminent:
            If enough power:
                Wait for tx window + offset
                transmit()
                

NOTE: Trying to conserve power for the TX
