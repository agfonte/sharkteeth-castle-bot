from dbmanager import DatabaseService
from utils import check_time, modificator, scripter, threshold, share_url, too_late, preparing
from mob import *
from datetime import datetime, timedelta
from botmarkup import gen_markup
import logging, copy, random
from telebot.types import InlineKeyboardMarkup,  InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[hunting]")



class HuntingManager:
    def __init__(self, bot, lang):
        super().__init__()
        self.bot = bot
        self.db = DatabaseService.get_instance()
        self.lang = lang
  
    def hunt(self, message):
        heros = self.db.heros
        if message.chat.type == "private":
            user = message.from_user.id
            if heros.find_one({"_id" : {"$eq": user}},{}):
                newvalues = { "$set": {"hunting": True} }
                heros.update_one({"_id" : user}, newvalues)
                self.bot.send_message(user, self.lang.get_value(user, "huntmsg"))
            else:
                self.bot.send_message(user, self.lang.get_value(user, "try_hunt_no_profile"))
    
    def setminlvl(self, message):
        heros = self.db.heros
        payload = message.text.split("/setminlvl")[1].strip()
        if message.chat.type == "private":
            user = message.from_user.id
            try:
                payload = int(payload)
                if payload < 0:
                    self.bot.send_message(user, self.lang.get_value(user, "error_positive_number"))
                    return
            except:
                self.bot.send_message(user, self.lang.get_value(user, "error_positive_number"))
                return
            
            if heros.find_one({"_id" : {"$eq": user}},{}):
                newvalues = { "$set": {"minlvl": payload} }
                heros.update_one({"_id" : user}, newvalues)
                self.bot.send_message(user, self.lang.get_value(user, "min_lvl_hunt")%payload)
            else:
                self.bot.send_message(user, "Sorry but i dont know you. Please try forward your /hero from @chtwrsbot.")
    
    def setmaxlvl(self, message):
        heros = self.db.heros
        payload = message.text.split("/setmaxlvl")[1].strip()
        if message.chat.type == "private":
            user = message.from_user.id
            try:
                payload = int(payload)
                if payload < 0:
                    self.bot.send_message(user, self.lang.get_value(user, "error_positive_number"))
                    return
            except:
                self.lang.get_value(user, "error_positive_number")
                return
            
            if heros.find_one({"_id" : {"$eq": user}},{}):
                newvalues = { "$set": {"maxlvl": payload} }
                heros.update_one({"_id" : user}, newvalues)
                self.bot.send_message(user, self.lang.get_value(user, "max_lvl_hunt")%payload)
            else:
                self.bot.send_message(user, self.lang.get_value(user, "no_profile"))
                
    def setallowmaxlvl(self, message):
        heros = self.db.heros
        payload = message.text.split("/sethelpmaxlvl")[1].strip()
        if message.chat.type == "private":
            user = message.from_user.id
            try:
                payload = int(payload)
                if payload < 0:
                    self.bot.send_message(user, "You should give me a positive number.")
                    return
            except:
                self.bot.send_message(user, "You should give me a positive number.")
                return
            
            if heros.find_one({"_id" : {"$eq": user}},{}):
                newvalues = { "$set": {"allowmaxlvl": payload} }
                heros.update_one({"_id" : user}, newvalues)
                self.bot.send_message(user, self.lang.get_value(user, "max_help")%payload)
            else:
                self.bot.send_message(user, self.lang.get_value(user, "no_profile"))

    def setallowminlvl(self, message):
        heros = self.db.heros
        payload = message.text.split("/sethelpminlvl")[1].strip()
        if message.chat.type == "private":
            user = message.from_user.id
            try:
                payload = int(payload)
                if payload < 0:
                    self.bot.send_message(user, self.lang.get_value(user, "error_positive_number"))
                    return
            except:
                self.bot.send_message(user, self.lang.get_value(user, "error_positive_number"))
                return
            
            if heros.find_one({"_id" : {"$eq": user}},{}):
                newvalues = { "$set": {"allowminlvl": payload} }
                heros.update_one({"_id" : user}, newvalues)
                self.bot.send_message(user, self.lang.get_value(user, "min_help")%payload)
            else:
                self.bot.send_message(user, self.lang.get_value(user, "no_profile"))
                
    def mystats(self, message):
        heros = self.db.heros
        if message.chat.type == "private":
            user = message.from_user.id
            x  = heros.find_one({"_id" : {"$eq": user}},{"name": 1, "guild": 1, "lvl": 1 ,  "maxlvl": 1,  "minlvl": 1, "allowmaxlvl": 1, "allowminlvl":1, "too_late": 1, "preparing": 1, "hunting": 1})
            if x:   
                status = ""        
                if x["hunting"]:
                    status = self.lang.get_value(user, "looking_for")
                else:
                    status = self.lang.get_value(user, "resting_from")
                self.bot.send_message(user, self.lang.get_value(user, "my_stats")%(x["name"], status, x["guild"], x["lvl"], x["maxlvl"], x["minlvl"], x["allowmaxlvl"], x["allowminlvl"], x["preparing"], x["too_late"]))
            else:
                self.bot.send_message(user, self.lang.get_value(user, "no_profile"))

    def stop(self, message):
        user = message.from_user.id
        heros = self.db.heros
        if message.chat.type == "private":
            if heros.find_one({"_id" : {"$eq": user}},{}):
                newvalues = { "$set": {"hunting": False} }
                heros.update_one({"_id" : user}, newvalues)
                self.bot.send_message(user, self.lang.get_value(user,"restmsg"))
            else:
                self.bot.send_message(user,self.lang.get_value(user,"no_profile"))
    
    def parse_mob(self, message):
        if message.text.startswith("You met some hostile creatures. Be careful:"):
            if check_time(message.forward_date, 3):
                self.bot.send_message(message.from_user.id, self.lang.get_value(message.from_user.id, "too_late"))
            else:
                self.mob(message.text, message.from_user.id, message.forward_date)
            return True
        return False
    
    def parse_preparing(self, message):
        text = message.text
        heros = self.db.heros

        id = message.from_user.id
        if text == preparing:
            h = heros.find_one({"_id" : {"$eq": id}},{"last_mob":1})
            try:
                msg = datetime.fromtimestamp(message.forward_date)
                lastm = h["last_mob"]
                logger.info(f"Hero: {id} - last_mob: {lastm} msg:{msg}, test:({msg > lastm}) calc:({ (msg - lastm).seconds / 60})")
                if msg > lastm and (msg - lastm).seconds / 60  < 3:
                    newvalues = { "$inc": {"preparing": 1}, "$set":{"last_mob": None} }
                    self.db.heros.update_one({"_id" : message.from_user.id}, newvalues)
                    self.bot.send_message(message.from_user.id, self.lang.get_value(message.from_user.id, "preparingmsg"))
                else:
                    self.bot.send_message(message.from_user.id, self.lang.get_value(message.from_user.id, "old_mob_result"))
            except Exception as e:  
                self.bot.send_message(message.from_user.id, self.lang.get_value(message.from_user.id, "old_mob_result"))
                logging.error("Exception occurred", exc_info=True)
    
    def parse_too_late(self, message):
        text = message.text
        heros = self.db.heros
        id = message.from_user.id
        try:
            if text == too_late:
                h = heros.find_one({"_id" : {"$eq": id}},{"last_mob": 1})
                msg = datetime.fromtimestamp(message.forward_date)
                lastm = h["last_mob"]
                logger.info(f"Hero: {id} - last_mob: {lastm} msg:{msg}, test:({msg > lastm}) calc:({ (msg - lastm).seconds / 60})")
                if msg > lastm and (msg - lastm).seconds / 60  < 3:
                    newvalues = { "$inc": {"too_late": 1}, "$set":{"last_mob": None}}
                    self.db.heros.update_one({"_id" : message.from_user.id}, newvalues)
                    self.bot.send_message(message.from_user.id, self.lang.get_value(message.from_user.id, "too_late_msg"))
                else:
                    self.bot.send_message(message.from_user.id, self.lang.get_value(message.from_user.id, "old_mob_result"))
        except Exception as e:
                self.bot.send_message(message.from_user.id, self.lang.get_value(message.from_user.id, "old_mob_result"))
                logging.error("Exception occurred", exc_info=True)
                
    def mob(self, text, id, fdate):
        mobs = Mobs()
        for line in text.splitlines()[1:]:
            if line != "" and not line.strip().startswith(modificator) and not line.strip().startswith("/fight_"):
                res = line.split("lvl.")
                mob = res[0].strip()
                lvl = int(res[1].strip())
                res = mob.split("x")
                amount = 1
                mob = ""
                if len(res)>1:
                    amount = int(res[0].strip())
                    mob = res[1].strip()
                else:
                    mob = res[0].strip()
                mobs.append(Mob(mob, lvl, amount, None))
            elif line.strip().startswith(modificator):
                mod = line.split(modificator)[1].strip()
                mobs.mobs[len(mobs.mobs)-1].set_mod(mod)
            elif line.startswith("/fight_"):
                self.call_helpers(mobs, line, id, fdate)
                
    def call_helpers(self, mob, line, id, fdate):
        heros = self.db.heros
        scripters = self.db.scripters
        media = 0
        for i in mob.mobs:
            media += int(i.lvl)

        media //=  len(mob.mobs)
        count = 0
        caller = heros.find_one({"_id" : {"$eq": id}},{"allowmaxlvl": 1, "lvl":1, "allowminlvl":1, "name": 1})
        helpers = []
        for h in heros.find({"_id":{"$ne": id}, "hunting":{"$eq": True}}):
            banned = scripters.find()
            
            t = datetime.today()
            blist = []
            for i in banned:
                if i["last"] + timedelta(days=i["times_detected"]) < t:
                    blist.append(i["_id"])
            
            huntreq = h["lvl"] + h["maxlvl"] >= media and h["lvl"] - h["minlvl"] <= media
            callreq = caller["lvl"] + caller["allowmaxlvl"] >= h["lvl"] and caller["lvl"] - caller["allowminlvl"] <= h["lvl"]
            
            logger.info("Caller : [" + caller["name"] + "]" + "requested help to: " + h["name"] +": "+ str(huntreq) +" "+ str(callreq))
            
            if huntreq and callreq and h["_id"] not in blist:
                helpers.append(h["_id"])
            last_mob = datetime.now()
            random.shuffle(helpers)
        try:
            self.bot.send_message(id, self.lang.get_value(id, "request_help")% len(helpers))
        except:
            logging.error("Exception occurred", exc_info=True)
        for i in helpers:
            user_lang = self.db.get_lang(h["_id"])
            try:
                
                d  = datetime.now() - datetime.fromtimestamp(fdate)
                remaining = d.seconds - 180
                self.bot.send_message(i, 
                                        self.lang.get_value(i, "fight_msg")%(caller["lvl"],mob.mobtext(), remaining), 
                                        reply_markup=gen_markup(line, self.lang.get_value(i, "unlock_fight")), 
                                        parse_mode="html")
            except:
                logging.error("Exception occurred", exc_info=True)
            
            logger.info("User id: " + str(i) + "  [" + self.lang.get_value(i, "fight_msg")%(caller["lvl"],mob.mobtext(), remaining) + "] " + str(datetime.now()))
        
        self.db.update_many({'_id':{'$in':helpers}}, {"$set":{"last_mob": last_mob}})
        logger.info("User id: " + str(id) + "  [requested to: " + str(count) + "] " + str(datetime.now()))
        
    def callback_hunt(self, call):
        heros = self.db.heros
        scripters = self.db.scripters
        scrip = copy.deepcopy(scripter)
        if call.data.startswith("/fight_"):
            user = call.from_user.id
            lapse = datetime.now()
            try:
                x = heros.find_one({"_id" : {"$eq": call.from_user.id}},{"last_mob": 1})
                diff = lapse - x["last_mob"]
                logger.info("User: " + str(call.from_user.id) + " [" + str(call.from_user.username) + "] unlocked fight ("+ str(diff.seconds) +")"  )
            except Exception as e:
                diff = threshold
                logging.error("Exception occurred", exc_info=True)

            if diff < threshold:
                scrip["_id"] = user
                scrip["last"] = lapse      
                scrip["times_detected"] = 0
                if not scripters.find_one({"_id" : {"$eq": user}},{}):
                    x = scripters.insert_one(scrip)      
                    bot.edit_message_text(chat_id=user,text=self.lang.get_value(user, "hi_scripter"), message_id=call.message.message_id)
                else:
                    newvalues = { "$set": {"last": lapse}, "$inc":{"times_detected": 1} }
                    scripters.update_one({"_id" : user}, newvalues)
                    scr = scripters.find_one({"_id" : {"$eq": user}},{"last": 1, "times_detected":1})
                    
                    new = timedelta(days=scr["times_detected"]) + scr["last"]
                    self.bot.edit_message_text(chat_id=user,text=self.lang.get_value(user, "ban_scripter_till")%(new.day, new.mon, new.year), message_id=call.message.message_id)
                self.bot.answer_callback_query(call.id, "")
                return
            self.bot.answer_callback_query(call.id, "")
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=self.lang.get_value(user, "fight"),url=share_url + call.data))
            try:
                self.bot.edit_message_text(chat_id=user,text=call.message.text, message_id=call.message.message_id,reply_markup=markup)
            except:
                logging.error("Exception occurred", exc_info=True)