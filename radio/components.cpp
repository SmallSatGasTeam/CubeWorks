#include "components.hpp"

Components::Components():
	// initialize everything to zero. If we are sending a picture we will override the picture data, but  we don't care about the others, so set everything to zero now and we can forget about the values we don't care about.
	// NEEDS Picture Data
	// First cursor.execute in database
	m_time(0),
	m_packet_type(0),
	m_mission_mode(0),
	m_reboot_count(0),
	m_boombox_uv(0),
	m_sp_x_pos_temp0(0),
	m_sp_z_pos_temp1(0),
	m_raspi_temp(0),
	m_eps_mcu_temp(0),
	m_batt_temp_cell0(0),
	m_batt_temp_cell1(0),
	m_batt_temp_cell2(0),
	m_batt_temp_cell3(0),
	m_batt_voltage(0),
	m_batt_current(0),
	m_bcr_voltage(0),
	m_bcr_current(0),
	m_eps_3v3_current(0),
	m_eps_5v_current(0),
	m_sp_x_voltage(0),
	m_sp_x_pos_current(0),
	m_sp_x_neg_current(0),
	m_sp_y_voltage(0),
	m_sp_y_pos_current(0),
	m_sp_y_neg_current(0),
	m_sp_z_voltage(0),

	// second cursor.execute in database
	m_la_x(0),
	m_la_y(0),
	m_la_z(0),

	// third cursor.execute in database
	m_ss_0(0),
	m_ss_1(0),
	m_ss_2(0),
	m_ss_3(0),
	m_ss_4(0),
	m_mf_x(0),
	m_mf_y(0),
	m_mf_z(0)
	{}