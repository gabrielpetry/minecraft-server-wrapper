# /bin/python3
from mcstatus import MinecraftServer
import sys
import time
import os
from pathlib import Path

CONTROL_FILE = '/tmp/players_online_control_file.txt'

# If you know the host and port, you may skip this and use MinecraftServer("example.org", 1234)
server = MinecraftServer.lookup("localhost:25565")
# 'status' is supported by all Minecraft servers that are version 1.7 or higher.
try:
    status = server.status()
    print("The server has {0} players and replied in {1} ms".format(
        status.players.online, status.latency))
except:
    # Server is still booting, so need to print return an ok
    exit(0)

# if there a player online modify the control file and return ok
if status.players.online > 0:
    # Update our control file on each execution of the script
    Path(CONTROL_FILE).touch()
    sys.exit(0)

# else, the file does not modify and we return error
sys.exit(1)

# the cron will check if the file was modified 10 minutes ago, after that shutsdown the server
# find /tmp/players_online_control_file.txt -mmin +10 -type f | grep -q . && shutdown -h now; /home/mcserver/shutdown.py
