#ifndef RADIO_DRIVER_HPP
#define RADIO_DRIVER_HPP

#include <vector>

class RadioDriver {
	public:
		RadioDriver(int duration);
		void transmit();
		std::vector<std::vector<int>> receive();
		std::vector<std::vector<int>> queryDB(bool pic);
		void packetize();
		void packetizePic();

	private:
			int m_lastTransTime; // in constructor set this to first boot time
			int m_duration;  
			std::vector<std::vector<int>> m_txWindows; //Change if necessary
			void unPacketizedData;
			std::vector<std::vector<int>> m_packets; //change if necessary, make class? maybe a std::variant


};

#endif
