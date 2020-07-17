#!/usr/bin/env python
# coding=utf-8

# @Su.Py~#_

import sys
import time
import re
import signal
import subprocess
import shlex
import json
from shell_colors import shell_colors as clr
import asyncio
import os


class server(object):
    """docstring for server"""

    def __init__(self, logger):
        super(server, self).__init__()

        java_memory = os.getenv("JAVA_MEMORY", "512M")
        server_executable = os.getenv("SERVER_EXECUTABLE", "server.jar")

        self.logger = logger
        self.process = False
        self.run_args = "java -Xms" + java_memory + " -Xmx" + java_memory + \
            " -XX:+UseConcMarkSweepGC -jar " + server_executable
        self.line = False
        self.clr_end = False
        self.log_user = False
        self.log_time = True
        self.log_warn = False
        self.log_err = False

    async def filters(self):
        color = ""

        self.line = re.sub(r"\[(\d{2}):(\d{2}):(\d{2})",
                           time.strftime("%I:%M:%S"), self.line)

        message_body = {
            "message": self.line
        }

        if(re.search(r"INFO\]:", self.line)):
            color = ""
            description = "info"
            # catch when users login

            # vanilla server
            regex_login = r"joined the game"
            regex_logout = r"left the game"

            if(re.search(regex_login, self.line)):

                username = re.split(regex_login, self.line)
                username = re.split(
                    r" \[Server thread\/INFO\]\: ", username[0])

                message_body = {
                    "username": username[1],
                    "action": "User login"
                }
                description = 'User login'

                # Forge server with simple login
                # username_ip = re.split(
                # r"\[Server thread\/INFO\] \[minecraft\/DedicatedServer\]: ", username_ip[0])

            # if not username_ip:
            #     username_ip = self.find_regex_in_line_and_return_split(
            #         r"\[Server thread\/ INFO\] \[minecraft\/ DedicatedServer\]: ")

            # catch user logout
            elif(re.search(regex_logout, self.line)):
                username = re.split(regex_logout, self.line)
                # username_ip = re.split(
                # r"\[Server thread\/INFO\] \[minecraft\/DedicatedServer\]: ", username_ip[0])
                username = re.split(
                    r" \[Server thread\/INFO\]\: ", username[0])
                message_body = {
                    "username": username[1],
                    "action": "User logout"
                }
                description = "User logout"

        elif(re.search(r"WARN\]:", self.line)):
            description = "warn"
            color = clr.warn

        elif(re.search(r"ERROR\]:", self.line)):
            description = "error"
            color = clr.err

        print("{0}{1}{2}".format(color, self.line, clr.end), end="")

        await self.logger.log(json.dumps(
            message_body
        ), description)

    def run(self):
        print("{0} {1}| SYSTM:{2} Starting the server...".format(
            time.strftime("%I:%M:%S"), clr.magenta, clr.end))
        try:
            self.process = subprocess.Popen(shlex.split(
                self.run_args), stdout=subprocess.PIPE, bufsize=1, cwd="server_directory/")
        except Exception as err:
            print("{0} {1}| SYSTM:{2}{3} ERROR: An error has occured while starting the server.{4}".format(
                time.strftime("%I:%M:%S"), clr.magenta, clr.end, clr.err, clr.end))
            print("{0} {1}| SYSTM:{2}{3}        {4}{5}".format(time.strftime(
                "%I:%M:%S"), clr.magenta, clr.end, clr.err, err, clr.end))

            return False
        else:
            print("{0} {1}| SYSTM:{2}{3} Successfully started the server.{4}".format(
                time.strftime("%I:%M:%S"), clr.magenta, clr.end, clr.green, clr.end))

        for self.line in iter(self.process.stdout.readline, b''):
            self.line = self.line.decode()
            try:
                asyncio.run(self.filters())
            except:
                error_message = sys.exc_info()
                asyncio.run(self.logger.log(
                    json.dumps({
                        "message": "unable to save current line",
                        "error": str(error_message)
                    }), "runtime error"))

        self.process.stdout.close()
        self.process.wait()
        self.process = False

    def quit(self, signal, frame):
        print("\n")
        print("{0} {1}| SYSTM:{2} Reviced exit command.".format(
            time.strftime("%I:%M:%S"), clr.magenta, clr.end))
        if(self.process):
            self.process.stdin.write("save-all\n".encode())
            print("{0} {1}| SYSTM:{2} Stopping the server...".format(
                time.strftime("%I:%M:%S"), clr.magenta, clr.end))
            self.process.stdin.write("stop\n".encode())
            for self.line in iter(self.process.stdout.readline, b''):
                self.line = self.line.decode()
                try:
                    asyncio.run(self.filters())
                except:
                    error_message = sys.exc_info()[0]
                    asyncio.run(self.logger.log(
                        {
                            "message": "unable to save current line",
                            "error": error_message
                        }
                    ), "runtime error")

            print("{0} {1}| SYSTM:{2} Server stopped.".format(
                time.strftime("%I:%M:%S"), clr.magenta, clr.end))
        print("{0} {1}| SYSTM:{2} Exiting.".format(
            time.strftime("%I:%M:%S"), clr.magenta, clr.end))
        sys.exit(0)
