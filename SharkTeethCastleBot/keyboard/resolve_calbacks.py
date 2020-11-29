from SharkTeethCastleBot.services import TelegramService, DatabaseService, LanguageService, HeroService
from SharkTeethCastleBot.settings import Settings
from .botmarkup import gen_add_to_squad, gen_whois_markup, gen_confirm_markup
import logging

logger = logging.getLogger("[cwapi_service]")
logging.basicConfig(level=logging.INFO)

def resolve_callbacks(callback):
    ts = TelegramService.getInstance()
    db = DatabaseService.getInstance()
    sett = Settings.getInstance()
    lang = LanguageService.getInstance()
    hero = HeroService.getInstance()
    data = callback.data
    user = callback.from_user.id
    
    username = callback.from_user.username
    if data.startswith("LANG_"):
        return sett.proccess_callback(callback)
    elif data.startswith("HERO_"):        
        res = False
        if data == "HERO_GEAR_UPDATE":
            res = db.update_gear(user)
        elif data == "HERO_UPDATE":
            res = db.update_hero(user, username)
        elif data.startswith("HERO_UPDATE_"):
            userid = int(data.split("HERO_UPDATE_")[1])
            res = db.update_hero(userid) + "_" + str(userid)
            user = userid
        elif data.startswith("HERO_GEAR_UPDATE_"):
            userid = int(data.split("HERO_GEAR_UPDATE_")[1])
            res = db.update_gear(userid) + "_" + str(userid)
            user = userid
        finalresponse = res
        if res.startswith("hero_updated"):
            finalresponse = "hero_updated"
        elif res.startswith("gear_updated"):
            finalresponse = "gear_updated"
        elif res.startswith("gear_not_auth"):
            finalresponse = "gear_not_auth"
        ts.bot.answer_callback_query(callback.id, lang.get_value(user, finalresponse))
        if res == "hero_updated" or res == "gear_updated":
            response = hero.me(user)
            try:
                ts.edit_message_text(
                    chat_id=callback.message.chat.id, 
                    text=response[0], 
                    message_id=callback.message.message_id,
                    params=response[1],
                    reply_markup=response[2])
            except:
                logging.error("ERROR EDITING MESSAGE", exc_info=True)
            return True
        elif res.startswith("hero_updated") or res.startswith("gear_updated"):
            userid = None
            if res.startswith("hero_updated"):
                userid = int(res.split("hero_updated_")[1])
            else:
                userid = int(res.split("gear_updated_")[1])
            answer, params, markup = hero.me(userid)
            markup = gen_whois_markup(userid, callback.message.chat.id)
            try:
                ts.edit_message_text(
                    chat_id=callback.message.chat.id, 
                    text=answer, 
                    message_id=callback.message.message_id,
                    params=params,
                    reply_markup=markup)
            except:
                logging.error("ERROR EDITING MESSAGE", exc_info=True)
            
        else:
            return False
    elif data.startswith("ADD_SQUAD_ID_"):
        userid = int(data.split("ADD_SQUAD_ID_")[1])
        ts.bot.answer_callback_query(callback.id, "")
        squads = db.squad.find({"squad": True})
        hero = db.heros.find_one({"_id": userid})
        list_squad = []
        for i in squads:
            short = i["short"]
            squadid  = i["_id"]
            list_squad.append((short, squadid))
            
        markup = gen_add_to_squad(userid, list_squad)
        
        ts.edit_message_text(
                    chat_id=callback.message.chat.id, 
                    text="select_squad",
                    params=("@" + hero["username"], ),
                    message_id=callback.message.message_id,
                    reply_markup=markup)
    elif data.startswith("SELECT_SQUAD_"):
        ts.bot.answer_callback_query(callback.id, "")
        squadid, userid = data.split("SELECT_SQUAD_")[1].split("_")
        squadid = int(squadid)
        userid = int(userid)
        hero = db.heros.find_one({"_id": userid})        
        if hero["squad"]:
            squad = hero["squad"]
            oldsquadid = squad["_id"]
            print(f"Id de chat {oldsquadid}, Id de usuario {userid}")
            try:
                if(ts.bot.kick_chat_member(squadid, userid)):
                    ts.send_message(userid, text="you_removed_from_squad", params=(squad["name"], squad["short"],))
            except Exception as e:
                # USER NO PARTICIPANT CAN HAPPEN
                logger.error(e)
        squad = db.squad.find_one({"_id": squadid})
        db.heros.update_one({"_id":userid}, {
            "$set":{
                "squad": {
                    "name": squad["name"],
                    "_id" : squad["_id"],
                    "short": squad["short"]
                }
            }
        })
        link = db.squad.find_one({"_id": squadid}, {"link": 1})["link"]
        
        try:
            ts.bot.unban_chat_member(squad["_id"], userid)
        except Exception as e:
            # USER NO PARTICIPANT CAN HAPPEN
            logger.error(e)

        ts.send_message(
                    callback.message.chat.id, 
                    text="hero_added_to_squad",
                    params=("@" + hero["username"], squad["name"], squad["short"]))
        ts.send_message(userid, text="you_added_to_squad", params=(squad["name"], link, squad["short"],))
    elif data.startswith("DEL_SQUAD_ID_"):
        userid = int(data.strip("DEL_SQUAD_ID_"))
        hero = db.heros.find_one({"_id": userid})
        squad = hero["squad"]
        if squad:
            ts.bot.kick_chat_member(squad["_id"], userid)
            db.heros.update_one({"_id":userid}, {
                "$set":{
                    "squad": None
                }
            })
            
            ts.send_message(
                        callback.message.chat.id, 
                        text="hero_removed_from_squad",
                        params=("@" + hero["username"], squad["name"], squad["short"]))
        
        ts.send_message(userid, text="you_removed_from_squad", params=(squad["name"], squad["short"],))
        ts.bot.answer_callback_query(callback.id, "")
        
    elif data.startswith("QUIT_SQUAD_CONFIRM"):
        ts.bot.answer_callback_query(callback.id, "Ok")
        if data == "QUIT_SQUAD_CONFIRM_YES":
            ts.bot.answer_callback_query(callback.id, "")
            userid = callback.from_user.id
            hero = db.heros.find_one({"_id": userid})
            squad = hero["squad"]
            if squad:
                ts.bot.kick_chat_member(squad["_id"], userid)
                db.heros.update_one({"_id":userid}, {
                    "$set":{
                        "squad": None
                    }
                })
                
                ts.send_message(
                            callback.message.chat.id, 
                            text="hero_removed_from_squad",
                            params=("@" + hero["username"], squad["name"], squad["short"]))
            ts.bot.answer_callback_query(callback.id, "")
    elif data.startswith("QUIT_SQUAD"):
        userid = callback.from_user.id
        ts.bot.answer_callback_query(callback.id, "")
        hero = db.heros.find_one({"_id": userid})
        squad = hero["squad"]
        confirmation = gen_confirm_markup(userid)
        ts.send_message(
                    callback.message.chat.id, 
                    text="quit_squad_confirm",
                    params=(squad["name"], squad["short"]),
                    reply_markup=confirmation
                    )
    
            