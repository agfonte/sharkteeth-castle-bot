from SharkTeethCastleBot.services import TelegramService, HeroService, DatabaseService, HeroService, StatsService
from SharkTeethCastleBot.settings import Settings
from SharkTeethCastleBot.keyboard.botmarkup import gen_bot_settings, gen_main_keyboard
import logging as log
import sys
import traceback

log.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log.INFO)
logger = log.getLogger(__name__)


def resolve_button_action(button, btns, userid, username):
    # logger.info(f'Se recibio este mensaje {button} se compara con {btns["me"]}')
    DatabaseService.get_instance().heros.find_one_and_update({"_id": userid}, {"$set": {"username": username}})
    if btns["me"] == button:
        button_me(userid)
    elif btns["settings"] == button:
        button_settings(userid)
    elif btns["back"] == button:
        button_back(userid)
    elif btns["lang"] == button:
        button_language(userid)
    elif btns["tops"] == button:
        button_tops(userid)
    elif btns["mysquad"] == button:
        button_mysquad(userid)


def button_language(userid):
    Settings.get_instance().select_language(userid)


def button_me(userid):
    # logger.info(f'Usando user id {userid} para obtener el hero')
    try:
        answer, params, markup = HeroService.getInstance().me(userid)
        if answer:
            # logger.info(f'Usando user id {userid} se obtuvo como respuesta {answer}')
            TelegramService.get_instance().send_message(userid, text=answer, params=params, reply_markup=markup)
    except:
        e = sys.exc_info()[0]
        trace = "".join(traceback.format_tb(sys.exc_info()[2]))
        logger.error(f"Error {e} {trace}")


def button_settings(userid):
    TelegramService.get_instance().send_message(userid, "welcome", reply_markup=gen_bot_settings(userid))


def button_back(userid):
    TelegramService.get_instance().send_message(userid, "welcome", reply_markup=gen_main_keyboard(userid))


def button_tops(userid):
    TelegramService.get_instance().send_message(userid, "welcome")


def button_mysquad(userid):
    StatsService.getInstance().mysquad(userid)
