#ifndef RADIO_DRIVER_HPP
#define RADIO_DRIVER_HPP

#include "components.hpp"

#include <vector>
#include <string>

class RadioDriver {
	public:
		RadioDriver(int duration);
		void transmit();
		std::vector<std::vector<int>> receive();
		std::vector<Components> queryDB(bool pic); //do we want a second function that only returns picture stuff instead of the whole class of unasigned values?
		void packetize();
		void packetizePic();

	private:
			int m_lastTransTime; // in constructor set this to first boot time
			int m_duration;  
			std::vector<std::vector<int>> m_txWindows; //Change if necessary
			std::vector<std::vector<std::string>> m_unPacketizedData; // must define data type
			std::vector<Components> m_packets; //change if necessary, make class? maybe a std::variant

};

#endif
