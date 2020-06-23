#include "radioDriver.hpp"

static int callback(void* data, int numRows, char** rows, char** colNames);

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

void RadioDriver::queryDB(bool pic, std::string query) {

	// if pic is true, get picture data.  else query database and put in unPacetizedData
	if (pic) {
		// run code to gather pic data from the database
	}
	else {
		//  run code to gather all other information from the database.
		// m_lastTransTime
		int exit = 0;
		exit = sqlite3_open("../db.sqlite3", &m_db);

		if (exit)
			std::cout << "failure" << std::endl;
		else
			std::cout << "success" << std::endl;

		int rc = sqlite3_exec(m_db, query.c_str(), callback, NULL, NULL);
		
		if (rc != SQLITE_OK)
			std::cout << "ERROR SELECT" << std::endl;
		else
			std::cout << "OPERATION OK!" << std::endl;
		
		sqlite3_close(m_db);
	}
}

void RadioDriver::packetize() {
	// packetize m_unPacketizedData an put it in m_packets
}

void RadioDriver::packetizePic() {
	// packetize the picture 
}

static int callback(void* data, int numRows, char** rows, char** colNames) {
	for (int i = 0; i < numRows; ++i) {
		std::cout << colNames[i] << " = " << rows[i] << std::endl;
	}
	return 0;
}
