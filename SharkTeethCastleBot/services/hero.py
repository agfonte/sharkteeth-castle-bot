from SharkTeethCastleBot.services import DatabaseService, TelegramService, CwApiService, AuthService, Permissions
import logging
from datetime import datetime, timezone
from SharkTeethCastleBot.utils.utils import correspondent_utc
from SharkTeethCastleBot.keyboard.botmarkup import gen_bot_settings, gen_main_keyboard, gen_hero_markup, gen_whois_markup
from SharkTeethCastleBot.utils.constants import emojis, levels, chatWarsBotId
from SharkTeethCastleBot.utils.utils import emoji_to_class, quality_to_letter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[hero_service]")

class HeroService:
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if HeroService.__instance == None:
            HeroService()
        return HeroService.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if HeroService.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            HeroService.__instance = self
            self.db = DatabaseService.getInstance()
            self.hero = self.db.heros
            self.ts = TelegramService.getInstance()
            self.cw = CwApiService.getInstance()

    
    def pledge(self, message, pledge):
        userid = message.from_user.id
        hero = self.exists(userid)
        
        if hero and message.forward_from.id == chatWarsBotId:
            if hero["pledge"]:
                self.ts.send_message(userid, "pledge_already_saved")
            else:
                self.hero.update_one({"_id": userid}, {"$set": {
                    "pledge": {
                        "invite":pledge, 
                        "date": datetime.fromtimestamp(message.forward_date)
                        }
                    }})
                self.ts.send_message(userid, "pledge_saved")
        elif hero:
            self.ts.reply_to(message, "not_forward")
        else:
            self.ts.send_message(userid, "first_steps")
    
    def no_pledge(self, message):
        userid = message.from_user.id
        h = self.exists(userid)
        if h and h["pledge"]:
            self.ts.send_message(message.from_user.id, "pledge_already_saved", reply_markup=gen_main_keyboard(message.from_user.id))
        elif h:
            self.ts.send_message(message.from_user.id, "no_pledge", reply_markup=gen_main_keyboard(message.from_user.id))
            for i in self.db.permissions.find_one({"_id": Permissions.COMMANDER})["list"]:
                try:
                    self.ts.send_message(i, "no_pledge_request", params=(message.from_user.username, userid), )
                except:
                    pass
        else:
            self.ts.send_message(message.from_user.id, "welcome_no_profile", reply_markup=gen_main_keyboard(message.from_user.id))
    
    def exists(self, userid):
        return self.db.heros.find_one({"_id": userid})
    
    def me(self, userid):
        hero = self.hero
        h = hero.find_one(userid)
        #logger.info(h)
        if h:
            in_castle_since = h["castle_since"].ctime()
            last_update = h["last_update"].ctime()
            pledge = h["pledge"]
            
            userid = h["_id"]
            gear = h["gear"]
            gearinfo = h["gear_info"]
            
            squad = h["squad"]
            short = None
            squadlink = ""
            if squad:
                squadlink = self.db.squad.find_one({"_id": squad["_id"]}, {"link": 1})["link"]
                short = squad["short"]
                squad = squad["name"]
                
            else:
                squad = "without squad"
            h = h["profile"]
            castle = h["castle"]
            atk = h["atk"]
            defs = h["def"]
            mana = h["mana"] if "mana" in h.keys() else None
            clas = h["class"]
            xp = h["exp"]
            gold = h["gold"]
            guild = None
            tag = None
            if "guild" in h.keys():
                guild = h["guild"]
                tag = h["guild_tag"]
            hp = h["hp"]
            lvl = h["lvl"]
            mana = h["mana"]
            maxHp = h["maxHp"]
            pogs = 0
            if "pouches" in h.keys():
                pogs = h["pouches"]
            stamina = h["stamina"]
            name = h["userName"]
            castle_name = "Sharkteeth Castle" #castle_by_emoji(castle)
            class_name = emoji_to_class(clas)
            uid = emojis["id"]
            guild_emoji = emojis["guild"]
            lvlemoji = emojis["rounded_medal"]
            fire = emojis["fire"]
            atkemoji = emojis ["cross_swords"]
            defemoji = emojis["shield"]
            goldemoji = emojis["gold"]
            
            gear_text = "🎽Equipment: %s/9 slots ⚔️%s🛡%s\n"
            gatk = 0
            gdef = 0
            gmana = 0
            amount = 0
            if gear:
                for i in gear.keys():
                    amount += 1
                    if "condition" in gearinfo[i].keys() and gearinfo[i]["condition"] == "broken":
                        gear_text += "🆘"
                    gear_text += gear[i]
                    if "quality" in gearinfo[i].keys():
                        gear_text +=  " (`"+ quality_to_letter(gearinfo[i]["quality"]) +"`) "
                    if "atk" in gearinfo[i].keys():
                        gatk += gearinfo[i]["atk"]
                        gear_text += "⚔️" + str(gearinfo[i]["atk"])
                        if "def" not in gearinfo[i].keys() and "mana" not in gearinfo[i].keys():
                            gear_text += "\n"
                    if "def" in gearinfo[i].keys():
                        gdef += gearinfo[i]["def"]
                        gear_text += "🛡" + str(gearinfo[i]["def"])
                        if "mana" not in gearinfo[i].keys():
                            gear_text += "\n"
                    if "mana" in gearinfo[i].keys():
                        gmana += gearinfo[i]["mana"]
                        gear_text += "💧" + str(gearinfo[i]["mana"])
                        gear_text += "\n"
                    if "def" not in gearinfo[i].keys() and "atk" not in gearinfo[i].keys():
                        gear_text += "\n"
                        
            gear_text = gear_text%(amount, gatk, gdef)
            answer = ""
            
            stats_line = ""
            if mana:
                stats_line = "%s: %i %s: %i %s: %i"%(atkemoji, atk, defemoji, defs, "💧", mana)
            else:
                stats_line = "%s: %i %s: %i"%(atkemoji, atk, defemoji, defs)
            if "guild" in h.keys():
                params = (
                    castle, name, castle_name, uid, userid, clas, class_name, 
                    guild_emoji, tag, guild, lvlemoji, int(lvl), fire,xp, levels[int(lvl)], 
                    levels[int(lvl)]-int(xp), stats_line, 
                    goldemoji, gold, pogs, gear_text, squad, squadlink, short, in_castle_since, last_update
                        )
                answer = "me_with_guild"
            else:
                
                params = (
                    castle, name, castle_name, uid, userid, clas, class_name, 
                    lvlemoji, int(lvl), fire,xp, levels[int(lvl)], 
                    levels[int(lvl)]-int(xp), stats_line,
                    goldemoji, gold, pogs, gear_text, squad, squadlink, short, in_castle_since, last_update
                        )
                answer = "me_no_guild"
            return (answer, params, gen_hero_markup(userid))
    
    def private_whois(self, userid, text):
            res = text.lstrip("/whois ")
            try:
                res = int(res)
                return self.whois(res, userid, userid)
            except:
                h = self.db.heros.find({"$or": [{"username": res[1:]},{"profile.userName": res}]})
                if h.count():
                    match = False
                    for i in h:
                        self.whois(i["_id"], userid, userid)
                        match = True
                    if match:
                        return
                else:
                    return self.ts.send_message(userid, "player_not_found")
                return self.ts.send_message(userid, "whois_wrong_parameters")
            
    def whois(self, userid, commanderid, chatid):
        if AuthService.getInstance().can_see_profile(userid, commanderid):
            answer, params, markup = self.me(userid)
            markup = gen_whois_markup(userid, commanderid)
            self.ts.send_message(commanderid, text=answer, params=params, reply_markup=markup)
        else:
            self.ts.send_message(chatid, userId=commanderid, text="no_authorized")
    
    
    def authed_hero(self, userid, username):
        basicprofile = self.cw.requestProfile(userid)
        self.db.insert_hero(userid, username, basicprofile)
        #requestGear = self.cw.requestGearInfo(userid)
        
    
    def authed_gear(self, userid, username):
        requestGear = self.cw.requestGearInfo(userid)
        response = self.db.insert_gear(userid, username, requestGear)
        
    def proccess_battle_report(self, userid, text, date):
        hero = self.hero.find_one({"_id": userid})
        lines = text.splitlines()
        firstline = lines[0].split(hero["profile"]["userName"])
        if len(firstline) == 1:
            return self.ts.send_message(userid, "change_name")
        else:
            name = firstline[0]
            stats = firstline[1]
            stats = stats.split(":")
            atk = stats[1].split("🛡")[0].strip()
            defs = stats[2].split("Lvl")[0].strip()
        gold = 0
        stock = 0
        exp = 0
        if "🔥Exp: " in lines[2]:
            exp = lines[2].split("🔥Exp: ")[1].strip()
            gold = lines[3].split("💰Gold: ")[1].strip()
            if "📦Stock: " in text:
                stock = lines[4].split("📦Stock: ")[1].strip()
        else:
            gold = lines[2].split("💰Gold: ")[1].strip()
            if "📦Stock: " in text:
                stock = lines[3].split("📦Stock: ")[1].strip()
        
        date = datetime.fromtimestamp(date, tz=timezone.utc)
        if self.report_exists(userid, date):
            return self.ts.send_message(userid, "report_already_saved")
        
        report = {
                    "exp":int(exp),
                    "gold": int(gold),
                    "atk": int(atk),
                    "def": int(defs),
                    "stock": int(stock),
                    "date": date
                }
        
        self.hero.update_one({"_id":userid},{
            "$push":{
                "reports_week": report,
                "last_week_report": report
                },
            "$inc": {
                "total_reports": 1
                }
            })
        return self.ts.send_message(userid, "report_saved")
        
    def parse_report(self, userid, report):
        pass
    
    def reports(self, userid):
        hero = self.hero.find_one({"_id": userid})
        print(hero["reports_week"][0]["date"].time())
        
    def report_exists(self, userid, date):
        hero = self.hero.find_one({"_id": userid})
        reports = hero["reports_week"]
        for i in reports:
            report = i["date"]
            if correspondent_utc(report.hour) == correspondent_utc(date.hour)\
                and report.day == date.day and report.year == date.year:
                return True
        return False