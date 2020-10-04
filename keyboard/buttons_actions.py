from services import TelegramService, HeroService, DatabaseService, HeroService, StatsService
from settings import Settings
from keyboard.botmarkup import gen_bot_settings, gen_main_keyboard

def resolve_button_action(button, btns, userid, username):
    DatabaseService.getInstance().heros.find_one_and_update({"_id":userid},{"$set":{"username":username}})
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
    Settings.getInstance().select_language(userid)

def button_me(userid):
    answer, params, markup = HeroService.getInstance().me(userid)
    if answer:
        TelegramService.getInstance().send_message(userid, text=answer, params=params, reply_markup=markup)

def button_settings(userid):
    TelegramService.getInstance().send_message(userid, "welcome", reply_markup=gen_bot_settings(userid))
    
def button_back(userid):
    TelegramService.getInstance().send_message(userid, "welcome", reply_markup=gen_main_keyboard(userid))
    
def button_tops(userid):
    TelegramService.getInstance().send_message(userid, "welcome")
    
def button_mysquad(userid):
    StatsService.getInstance().mysquad(userid)