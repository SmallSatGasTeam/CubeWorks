#include "radioDriver.hpp"

RadioDriver::RadioDriver(int duration):
	m_duration(duration)
{
	// query db for first boot time set m_lastTransTime to it.
}

void RadioDriver::transmit() {
	// radio hardware initialization, send m_packets to radio 
}

std::vector<std::vector<int>> RadioDriver::receive() {
	// main maybe calls this on loop to watch radio?
}

std::vector<std::vector<int>> RadioDriver::queryDB(bool pic) {
	// if pic is true, get picture data.  else query database and put in unPacetizedData
}

void RadioDriver::packetize() {
	// packetize m_unPacketizedData an put it in m_packets
}

void RadioDriver::pacetizePic() {
	// packetize the picture 
}
