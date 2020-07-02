#ifndef TX_WINDOW_HPP
#define TX_WINDOW_HPP

class TXWindow {
	public:
		TXWindow(int start, int duration);
		int getStart();
		int getEnd();
		int getDuration();

	private:
		int m_start;
		int m_duration;
		int m_end;
};

#endif
