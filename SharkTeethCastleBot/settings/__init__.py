import logging
import os

from .settings import Settings

settings = Settings().get_instance()
logger = logging.getLogger("[settings]")

try:
    cwuser = os.environ["CW_USER"]
    cwpass = os.environ["CW_PASS"]
    settings.set_env(cwuser, cwpass)
except:
    logging.error("Failed to load env variables", exc_info=True)
