from settings.settings import Settings
import os, logging

settings = Settings().getInstance()
logger = logging.getLogger("[settings]")

try:
    cwuser = os.environ["CW_USER"]
    cwpass = os.environ["CW_PASS"]
    settings.setEnv(cwuser, cwpass)
except:
    logging.error("Failed to load env variables", exc_info=True)    





        
        