import logging as log
from time import sleep
import SharkTeethCastleBot.main
from multiprocessing import Process

log.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log.INFO)
logger = log.getLogger(__name__)


def loop_f():
    while 1:
        sleep(0.01)
        SharkTeethCastleBot.main.bot_main()


if __name__ == '__main__':
    Process(target=loop_f).start()
