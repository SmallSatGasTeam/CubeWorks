import os


def measureCpuTemp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))
