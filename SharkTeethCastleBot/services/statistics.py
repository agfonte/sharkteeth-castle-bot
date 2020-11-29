from SharkTeethCastleBot.services import DatabaseService, TelegramService, AuthService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[hunting]")

class StatsService:
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if StatsService.__instance == None:
            StatsService()
        return StatsService.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if StatsService.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            StatsService.__instance = self
            self.db = DatabaseService.get_instance()
            self.ts = TelegramService.get_instance()

    def top_hunters(self, user):
        heros = self.db.heros.find().sort("preparing", -1).limit(10)
        res = self.lang.get_value(user, "top_hunters") + "\n"
        i = 1
        for h in heros:
            res+= "#" + str(i) + " - " + h["name"] + " : " + str(h["preparing"]) + "\n"
            i += 1
        logging.info(res)
        self.bot.send_message(user, res)
        
    def mysquad(self, userid):
        hero = self.db.heros.find_one({"_id": userid})
        if hero:
            squad = hero["squad"]
            if squad:
                list_squad = self.db.heros.find({"squad._id": squad["_id"]})
                detail_squad = self.db.squad.find_one({"_id": squad["_id"]})
                commander = detail_squad["commander"]["username"]

                maxplayers = list_squad.count()
                role = AuthService.getInstance().get_role(userid)
                if role[0] in ["SQUAD_LEADER", "COMMANDERS"]:
                    atk = 0
                    defs = 0
                    mana = 0
                    for i in list_squad:
                        atk += i["profile"]["atk"]
                        defs += i["profile"]["def"]
                        mana += i["profile"]["def"] if "mana" in i["profile"].keys() else 0
                    return self.ts.send_message(userid, "squad_message_leader", 
                                                params=(detail_squad["name"], 
                                                        detail_squad["short"],
                                                        commander, 
                                                        detail_squad["link"],
                                                        maxplayers,
                                                        atk, defs, mana))
                else:
                    return self.ts.send_message(userid, "squad_message_soldier", 
                                                params=(detail_squad["name"], 
                                                        detail_squad["short"],
                                                        commander, 
                                                        detail_squad["link"],
                                                        maxplayers))
            else:
                return self.ts.send_message(userid, "no_squad")
        else:
            return self.ts.send_message(userid, "no_profile")
        