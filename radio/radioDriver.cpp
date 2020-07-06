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


	// GET THE DATA FROM PRESTEN AND THEN CALL QUERY DB WHICH THEN SENDS TO PACKETIZE
	// MAKE THIS FUNCTION TTHE DRIVER?? OR DO IT IN THE MAIN FUNCTION???
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

			// NOTES FROM SHAWN:
	// THIS WILL BE RECIEVED FROM A python
	// check 1: power check eps driver
	// check 2: decode the message. what type if picture what number of picture?
	// check 3: Check and set transmission windows 
	// check 4: How many bytes are we going to transmit 

	// datatype, transmission windows, and ifPic will be passed in as command line arguments.
	// call delay function to delay until we hit trasmission window. 5 seconds before call shawn's function
	// pass to shawn datatype and how many lines we are trasmitting from the file. 
	// Communicate with shawn the exact file path and the file name. 

	// CREATE THIS CLASS AS AN EXECUTABLE THAT ACCEPTS THE REQUIRED PARAMETERS AS COMMAND LINE ARGUMENTS
	// GET FROM SHAWN THE NAME OF HIS EXECUTABLE AND CALL IT IN THIS CLASS PASSING THE REQUIRED PARAMETERS AS COMMNAD LINE ARGUMENTS

    /////////////////////////////////////////////////////////////////

	// packetize m_unPacketizedData an put it in m_packets
    // move from std::vector<std::vector<std::string>> to the class. 


	// send 128 bytes to each line of the transmit file. Count how many lines and store that in a header. Erase old file before writing.
}

void RadioDriver::packetizePic() {
	// packetize the picture 
}
