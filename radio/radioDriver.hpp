#ifndef RADIO_DRIVER_HPP
#define RADIO_DRIVER_HPP

#include <vector>
#include <string>
#include <sqlite3.h>
#include <iostream>

#include "packet.hpp"
#include "txWindow.hpp"

class RadioDriver {
	public:
		RadioDriver(int duration);
		void transmit();
		std::vector<std::vector<int>> receive();
		void queryDB(bool pic, std::string query); //do we want a second function that only returns picture stuff instead of the whole class of unasigned values?
		void packetize();
		void packetizePic();

	private:
			int m_lastTransTime; // in constructor set this to first boot time
			int m_duration;  
			std::vector<std::vector<int>> m_txWindows; //Change if necessary
			std::vector<std::vector<std::string>> m_unPacketizedData; // must define data type
			std::vector<Packet> m_packets; //change if necessary, make class? maybe a std::variant
			sqlite3* m_db;

};

#endif
