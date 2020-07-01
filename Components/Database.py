from Components.Component import Component
import sqlite3
from datetime import datetime

class Database(Component):
    """
    A database class that implements database creation and methods to read and write from the database. Creates the following tables: 
    1. firstBoot
    2. picture
    3. attitudeDetermination
    4. data
    5. housekeeping
    """
    def __init__(self):
        """
        Initializes a Database object, calls the parent constructor, and connects to a sqlite3 database.
        """
        super().__init__("Database", 1)
        self.connection = sqlite3.connect('db.sqlite3')
        self.initdb()


    def update(self, context):
        """
        Concrete implementation of Component.update().
        Takes a dictionary (context) as a parameter, and writes it to a new row in the database.  
        """
        self.commitPicture(context)
        self.commitTTNC(context)
        self.commitBoomDeploy(context)
        self.commitAttitude(context)


    def getFirstBoot(self):
        """
        Queries the firstBoot table in the database and returns the firstBoot value if it exists.
        If no firstBoot value exists, returns None.
        """
        cursor = self.connection.execute("SELECT * FROM first_boot")
        rows = cursor.fetchall()
        if len(rows) == 0:
            return None
        return rows[0][0]


    def setFirstBoot(self, time):
        """
        Takes a datetime string as a parameter and inserts
        it into the firstBoot table in the database.  
        """
        insertCommand = """INSERT INTO firstBoot VALUES (?);"""
        self.connection.execute("INSERT INTO first_boot VALUES(?)", (time,))
        self.connection.commit()


    def commitPicture(self, context):
        """
        Parses context and commits relevant picture data to db.
        1. check for all relevant keys in context
        2. if key exists, put it in the pre-commit data string
        3. else, put a default value in the string
        4. commit string
        """


    def commitTTNC(self, context):
        """
        Parses context and commits relevant TT&C (Telemetry, Tracking, and Command) data to db.
        """
        time = 0
        packet_type = 0
        mission_mode = 0
        reboot_count = 0
        boombox_uv = 0.0
        sp_x_pos_temp0= 0.0
        sp_z_pos_temp1= 0.0
        raspi_temp = 0.0
        eps_mcu_temp = 0.0
        batt_temp_cell0 = 0.0
        batt_temp_cell1 = 0.0
        batt_temp_cell2 = 0.0
        batt_temp_cell3 = 0.0
        batt_voltage = 0.0
        batt_current = 0.0
        bcr_voltage = 0.0
        bcr_current = 0.0
        eps_3v3_current = 0.0
        eps_5v_current = 0.0
        sp_x_voltage = 0.0
        sp_x_pos_current = 0.0
        sp_x_neg_current = 0.0
        sp_y_voltage = 0.0
        sp_y_pos_current = 0.0
        sp_y_neg_current = 0.0
        sp_z_voltage = 0.0

        if ('rtc' in context):
            time = context['rtc']

        self.connection.execute("INSERT INTO ttnc (time, packet_type, mission_mode, reboot_count, boombox_uv, sp_x_pos_temp0, sp_z_pos_temp1, raspi_temp, eps_mcu_temp, batt_temp_cell0, batt_temp_cell1, batt_temp_cell2, batt_temp_cell3, batt_voltage, batt_current, bcr_voltage, bcr_current, eps_3v3_current, eps_5v_current, sp_x_voltage, sp_x_pos_current, sp_x_neg_current, sp_y_voltage, sp_y_pos_current, sp_y_neg_current, sp_z_voltage)VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            time,
            packet_type,
            mission_mode,
            reboot_count,
            boombox_uv,
            sp_x_pos_temp0,
            sp_z_pos_temp1,
            raspi_temp,
            eps_mcu_temp,
            batt_temp_cell0,
            batt_temp_cell1,
            batt_temp_cell2,
            batt_temp_cell3,
            batt_voltage,
            batt_current,
            bcr_voltage,
            bcr_current,
            eps_3v3_current,
            eps_5v_current,
            sp_x_voltage,
            sp_x_pos_current,
            sp_x_neg_current,
            sp_y_voltage,
            sp_y_pos_current,
            sp_y_neg_current,
            sp_z_voltage))
        self.connection.commit()

  

    def commitBoomDeploy(self, context):
        """
        Parses context and commits relevant boom deployment data to db.
        """
        time = 0
        packet_type = 0
        boombox_uv = 0.0
        la_x = 0.0
        la_y = 0.0
        la_z = 0.0

        if ('rtc' in context):
            time = context['rtc']
        if ('packet_type' in context):
            pass
        if ('boombox_uv' in context):
            pass
        if ('la_x' in context):
            pass
        if ('la_y' in context):
            pass
        if ('la_z' in context):
            pass
        
        self.connection.execute("INSERT INTO boom_deploy (time, packet_type, boombox_uv, la_x, la_y, la_z) VALUES (?,?,?,?,?,?)", (
            time, 
            packet_type, 
            boombox_uv, 
            la_x, 
            la_y, 
            la_z))
        self.connection.commit()


    def commitAttitude(self, context):
        """
        Parses context and commits relevant attatude data to db.
        """
        time = 0
        packet_type = 0
        ss_0 = 0.0
        ss_1 = 0.0
        ss_2 = 0.0
        ss_3 = 0.0
        ss_4 = 0.0
        mf_x = 0.0
        mf_y = 0.0
        mf_z = 0.0

        if ('rtc' in context):
            time = context['rtc']
        # Sorry this is ugly.  SQLite3 expects a string literal that can't be broken up.
        self.connection.execute("INSERT INTO attitude (time, packet_type, ss_0, ss_1, ss_2, ss_3, ss_4, mf_x, mf_y, mf_z) VALUES (?,?,?,?,?,?,?,?,?,?)", (
            time, 
            packet_type, 
            ss_0, 
            ss_1, 
            ss_2, 
            ss_3, 
            ss_4, 
            mf_x, 
            mf_y, 
            mf_z))
        self.connection.commit()



    def initdb(self):
        """
        Creates database tables if they don't exist.
        1. A firstBoot table that stores only the first boot time
        2. A picture table that stores the filepaths of various photos taken
        3. A data table that stores datapoints taken by the sensors
        Note that the "+" and "-" characters will cause SQLite to emit a syntax error if 
        put in a column name
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS first_boot
            (time int PRIMARY KEY)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS picture
            (time int PRIMARY KEY,
            text path,
            int packetNum,
            blob packet)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ttnc
            (time int PRIMARY KEY,
            packet_type int,
            mission_mode int,
            reboot_count int,
            boombox_uv float,
            sp_x_pos_temp0 float,
            sp_z_pos_temp1 float,
            raspi_temp float,
            eps_mcu_temp float,
            batt_temp_cell0 float,
            batt_temp_cell1 float,
            batt_temp_cell2 float,
            batt_temp_cell3 float,
            batt_voltage float,
            batt_current float,
            bcr_voltage float,
            bcr_current float,
            eps_3v3_current float,
            eps_5v_current float,
            sp_x_voltage float,
            sp_x_pos_current float,
            sp_x_neg_current float,
            sp_y_voltage float,
            sp_y_pos_current float,
            sp_y_neg_current float,
            sp_z_voltage float)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS boom_deploy
            (time int PRIMARY KEY,
            packet_type int,
            boombox_uv float,
            la_x float,
            la_y float,
            la_z float)''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attitude
            (time int PRIMARY KEY,
            packet_type float,
            ss_0 float,
            ss_1 float,
            ss_2 float,
            ss_3 float,
            ss_4 float,
            mf_x float,
            mf_y float,
            mf_z float)''')

        self.connection.commit()
