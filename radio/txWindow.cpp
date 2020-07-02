#include "txWindow.hpp"

TXWindow::TXWindow(int start, int duration):
	m_start(start),
	m_duration(duration)

{
	m_end = m_start + m_duration;
}

int TXWindow::getStart() {
	return m_start;
}

int TXWindow::getEnd() {
	return m_end;
}

int TXWindow::getDuration() {
	return m_duration;
}
