import subprocess

with open("log.txt", "a") as f:
    f.write("Booted")

#cmd = 'python3 testLog.py &'
cmd = 'python3 watchdog/Heartbeat/testHeartbeat.py &'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
