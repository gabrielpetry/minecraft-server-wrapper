from server import server
import sys
import signal
import time
from shell_colors import shell_colors as clr
from logger import logger
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

if __name__ == '__main__':
    logger = logger()
    svr = server(logger)
    signal.signal(signal.SIGINT, svr.quit)

    run = svr.run()
