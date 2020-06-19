#include "radioDriver.hpp"

RadioDriver::RadioDriver(int duration):
	m_duration(duration),
	m_lastTransTime(0)
{
	// query db for first boot time set m_lastTransTime to it.
	// start loop to run recieve function
}

void RadioDriver::transmit() {
	// radio hardware initialization, send m_packets to radio 
	// update lastTransTime
}  

std::vector<std::vector<int>> RadioDriver::receive() {
	// main maybe calls this on loop to watch radio?
	
	std::vector<std::vector<int>> testOuter;
	std::vector<int> testInner;
	testOuter.push_back(testInner);
	return testOuter;
}

std::vector<Components> RadioDriver::queryDB(bool pic) {

	// if pic is true, get picture data.  else query database and put in unPacetizedData
	if (pic) {
		// run code to gather pic data from the database
	}
	else {
		//  run code to gather all other information from the database.
		// m_lastTransTime
	}

	Components compTest;
	std::vector<Components> test;
	test.push_back(compTest);
	return test;
}

void RadioDriver::packetize() {
	// packetize m_unPacketizedData an put it in m_packets
}

void RadioDriver::packetizePic() {
	// packetize the picture 
}
