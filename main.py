import logging as log
from time import sleep
import SharkTeethCastleBot.main as sharkTeethCastleBot

log.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log.INFO)
logger = log.getLogger(__name__)

from multiprocessing import Process
""" import psutil """

def loop_f():
    while 1:
        sleep(0.01)
        sharkTeethCastleBot.bot_main()

if __name__ == '__main__':
    p6 = Process(target=loop_f).start()