import telebot, logging, os, threading, multiprocessing
from multiprocessing import Pool,Process
from datetime import datetime, timedelta
from services import LanguageService, TelegramService, SquadService, HeroService, SchedulingService
from utils.constants import commands as cmd, chatWarsBotId, private_commands
from threading import Thread
from utils.utils import isCommand,  parseCodeAuth, all_buttons, is_battle_report, check_if_pledge
from keyboard.botmarkup import gen_main_keyboard
from keyboard.buttons_actions import resolve_button_action
from keyboard.resolve_calbacks import resolve_callbacks
from services import CwApiService
from settings import Settings
# LOGGIN
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("[sharkteeth_core]")
logging.getLogger("pika").propagate = False
#BOT CORE
bot = TelegramService.getInstance().setBot(telebot.TeleBot(os.environ["HUNTER_TOKEN"], "html"))
schedule = SchedulingService.getInstance()


logger.info('Starting app...')

#DEBUG
debug = "false"
try:
    debug = os.environ["DEBUG"]
    if debug:
        logging.warning("DEBUG MODE: TRUE")
    else:
        logging.warn("DEBUG MODE: FALSE")
except:
    logging.warn("DEBUG MODE: FALSE")


@bot.bot.message_handler(commands=["start"])
def start(message):
    userid = message.from_user.id
    username = message.from_user.first_name
    usertag = message.from_user.username
    hero = HeroService.getInstance().exists(userid)
    if hero:
        bot.send_message(message.from_user.id, "welcome", reply_markup=gen_main_keyboard(message.from_user.id))
    else:
        bot.send_message(message.from_user.id, "welcome_no_profile", reply_markup=gen_main_keyboard(message.from_user.id))
        


@bot.bot.message_handler(content_types=[
    "new_chat_members"
])
def new_user(message):
    userid = message.from_user.id
    isBot = message.from_user.is_bot
    if not isBot and not SquadService.getInstance().can_enter(userid, message.chat.id):
        if bot.bot.kick_chat_member(message.chat.id, userid):
            username = message.from_user.username
            name = message.from_user.first_name
            squad = SquadService.getInstance().squad_info(message.chat.id)
            bot.send_message(message.chat.id, "enter_squad_forbidden", params=(name, username, userid, squad["name"], squad["short"]),)
    elif not isBot:
        bot.bot.reply_to(message, "Welcome pal")

@bot.bot.message_handler(commands=cmd.keys())
def commands(message):
    if message.chat.type == "private" and message.from_user.username is None:
        return bot.reply_to(message, "no_username")
    
    if message.content_type == "text":
        comm = isCommand(message.text)
        if message.chat.type == "private":
            if comm in private_commands.values():
                if comm == "/start":    
                    bot.send_message(message.from_user.id, "welcome", reply_markup=gen_main_keyboard(message.from_user.id))
                if comm == "/first_steps":
                    bot.send_message(message.from_user.id, "first_steps", reply_markup=gen_main_keyboard(message.from_user.id))
                if comm == "/no_pledge":
                    HeroService.getInstance().no_pledge(message)
                if comm == "/auth":
                    bot.send_message(message.from_user.id, "auth_request")
                    CwApiService.getInstance().auth(message.from_user.id)
                if comm == "/gearAuth":
                    bot.send_message(message.from_user.id, "auth_request")
                    CwApiService.getInstance().authRequestGearInfo(message.from_user.id)
                if comm == "/reports":
                    HeroService.getInstance().reports(message.from_user.id)
                if comm == "/add":
                    SquadService.getInstance().add_private_to_squad(message)
                if comm == "/whois":
                    HeroService.getInstance().private_whois(message.from_user.id, message.text)
            else:
                pass
        else:
            if comm:
                if comm == "/create_squad":
                    SquadService.getInstance().create_squad(message, comm)
                if comm == "/kick" and message.reply_to_message is not None:
                    replied_msg = message.reply_to_message
                    replied_usrid = replied_msg.from_user.id
                    replied_usrname = replied_msg.from_user.username
                    bot.bot.kick_chat_member(message.chat.id, replied_usrid)
                    bot.send_message(message.chat.id, "user_kicked", params=(replied_usrname), userId=message.from_user.id)
                if comm == "/auth":
                    bot.send_message(message.from_user.id, "auth_request")
                    CwApiService.getInstance().auth(message.from_user.id)
                if comm == "/gearAuth":
                    bot.send_message(message.from_user.id, "auth_request")
                    CwApiService.getInstance().authRequestGearInfo(message.from_user.id)
                if comm == "/whois" and message.reply_to_message is not None:
                    replied_msg = message.reply_to_message
                    userid = message.from_user.id
                    replied_usrid = replied_msg.from_user.id
                    replied_usrname = replied_msg.from_user.username
                    logging.info("/whois on user: " + str(replied_usrid))
                    HeroService.getInstance().whois(replied_usrid, userid, message.chat.id)
                if comm == "/add":
                    SquadService.getInstance().add_to_squad_by_join(message)
                
                          

@bot.bot.message_handler(func=lambda m: True)
def update(message):
    
    cwapi = CwApiService.getInstance()
    code = parseCodeAuth(message.text)
    if code:
        return proccess_auth_code(message, code)
        
    if is_battle_report(message.text):
        return HeroService.getInstance().proccess_battle_report(message.from_user.id, message.text, message.forward_date)
    pledge = check_if_pledge(message.text)
    if pledge:
        return HeroService.getInstance().pledge(message, pledge)
    
    if message.chat.type == "private" and message.from_user.username is None:
        return bot.reply_to(message, "no_username")
    
    
    btns = all_buttons(message.from_user.id)
    if message.chat.type == "private" and message.text in btns.values():
        btn = message.text
        return resolve_button_action(btn, btns, message.from_user.id, message.from_user.username)
        
    #if message.forward_from is not None and message.forward_from.id == chatWarsBotId:
     #   if is_battle_report(message.text):
      #      return
       # if hunting.parse_mob(message):
        #    return
        #if hunting.parse_preparing(message):
         #   return
        #if hunting.parse_too_late(message):
         #   return


@bot.bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    resolve_callbacks(call)


def proccess_auth_code(message, code):
    cwapi = CwApiService.getInstance()
    if " - view currently equipped gear" not in message.text:
        if cwapi.grantToken(message.from_user.id, code) == "Ok":
            usrid = message.chat.id
            params = None
            if message.chat.type == "private":
                usrid = message.from_user.id
                markup = gen_main_keyboard(usrid)
                bot.send_message(usrid, "auth_completed", reply_markup=markup)
            else:
                params = (message.from_user.username)
                bot.send_message(usrid, "auth_completed_public", params=params)
            HeroService.getInstance().authed_hero(usrid, message.from_user.username)
        else:
           bot.send_message(usrid, "try_later")

    if " - view currently equipped gear" in message.text:
        usrid = message.chat.id
        if cwapi.grantAdditionalOperation(message.from_user.id, code) == "Ok":
            params = None
            if message.chat.type == "private":
                usrid = message.from_user.id
                bot.send_message(usrid, "auth_completed_gear")   
            else:
                params = (message.from_user.username)
                TelegramService.getInstance().send_message(usrid, "auth_completed_gear_public", params=params)   
            HeroService.getInstance().authed_gear(usrid, message.from_user.username)
        else:
            bot.send_message(usrid, "try_later")


def bot_main():
    logger.info("Polling")
    #bot.bot.infinity_polling(True)
    bot_thread = threading.Thread(target=bot.bot.infinity_polling,kwargs=dict(none_stop=True))
    bot_thread.start()
    #schedule.start()
    print(threading.currentThread().getName())
    #bot.bot.polling()
    


if __name__ == '__main__':
    bot_main()
    


