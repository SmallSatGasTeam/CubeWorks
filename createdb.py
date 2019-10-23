import sqlite3

connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()
try:
    cursor.execute('''
        CREATE TABLE firstBoot
        (time timestamp PRIMARY KEY) [without rowid]''')
except:
    pass

try:
    cursor.execute('''
        CREATE TABLE picture
        (time timestamp PRIMARY KEY,
        filepath text) [without rowid]''')
except:
    pass

try:
    cursor.execute('''
        CREATE TABLE data
        (time timestamp PRIMARY KEY,
        uvintensity float,
        boomdeployed bool,
        magx float,
        magy float,
        magz float,
        magxr float,
        magyr float,
        magzr float,
        battvoltage float,
        therm0 float,
        therm1 float,
        therm2 float,
        therm3 float,
        therm4 float,
        therm5 float,
        therm6 float,
        powermode int) [without rowid] ''')

except:
    pass

connection.commit()
