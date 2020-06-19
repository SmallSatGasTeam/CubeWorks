#ifndef COMPONENTS_HPP
#define COMPONENTS_HPP

class Components {
	friend class RadioDriver;
public:
	Components();
	// NEEDS Picture Data

	// First cursor.execute in database
	int m_time;
	int m_packet_type;
	int m_mission_mode;
	int m_reboot_count;
	float m_boombox_uv;
	float m_sp_x_pos_temp0;
	float m_sp_z_pos_temp1;
	float m_raspi_temp;
	float m_eps_mcu_temp;
	float m_batt_temp_cell0;
	float m_batt_temp_cell1;
	float m_batt_temp_cell2;
	float m_batt_temp_cell3;
	float m_batt_voltage;
	float m_batt_current;
	float m_bcr_voltage;
	float m_bcr_current;
	float m_eps_3v3_current;
	float m_eps_5v_current;
	float m_sp_x_voltage;
	float m_sp_x_pos_current;
	float m_sp_x_neg_current;
	float m_sp_y_voltage;
	float m_sp_y_pos_current;
	float m_sp_y_neg_current;
	float m_sp_z_voltage;

	// second cursor.execute in database
	float m_la_x;
	float m_la_y;
	float m_la_z;

	// third cursor.execute in database
	float m_ss_0;
	float m_ss_1;
	float m_ss_2;
	float m_ss_3;
	float m_ss_4;
	float m_mf_x;
	float m_mf_y;
	float m_mf_z;

	// Get functions for each of these packets
};

#endif
