from pymongo import collection
import os, pymongo, logging

from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[database]")


class DatabaseService:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DatabaseService.__instance is None:
            DatabaseService()
        return DatabaseService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DatabaseService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseService.__instance = self
            self.client = pymongo.MongoClient(os.environ["MONGODB_URI"])
            self.db = self.client[os.environ["DATABASE_NAME"]]
            self.heros = self.db["hero"]
            self.herosettings = self.db["herosettings"]
            self.auth = self.db["auth"]
            self.squad = self.db["squad"]
            self.permissions = self.db["permissions"]
            self.scripters = self.db["scripters"]
            self.commanders = self.db["commanders"]
            self.lang_cache = dict()

    def is_hero_auth(self, userid):
        user = self.auth.find_one({"_id": userid})
        return user

    def update_token(self, userid, token):
        self.auth.update({"_id": userid}, {"cwtoken": token})

    def insert_authed_user(self, userid, cwid, token):
        import SharkTeethCastleBot.services as services
        if self.auth.find_one({"_id": userid}) is None:
            self.auth.insert_one({
                "_id": userid,
                "cwid": cwid,
                "cwtoken": token
            })
            self.permissions.insert_one({"_id": userid,
                                         services.Permissions.SQUAD_LEADER: [],
                                         services.Permissions.GUILD_LEADER: None,
                                         services.Permissions.MODERATOR: []
                                         }
                                        )
            self.herosettings.insert_one({"_id": userid,
                                          "LANG": "EN",
                                          "exchange_sellings": False,
                                          "stock_changes": False
                                          })
        else:
            self.auth.update_one({"_id": userid}, {"$set": {
                "cwid": cwid,
                "cwtoken": token
            }})

    def add_permissions_to(self, userid, permission, squadid):
        pass

    def get_token_by_user(self, userid):
        return self.auth.find_one({"_id": userid}, {"cwtoken": 1})["cwtoken"]

    def insert_hero(self, userid, username, hero):
        h = self.heros.find_one({"_id": userid})
        if h:
            self.heros.update_one({"_id": userid}, {"$set": {
                "last_update": datetime.now(),
                "profile": hero["profile"]
            }
            })
        else:
            thero = {
                "_id": userid,
                "username": username,
                "castle_since": datetime.now(),
                "last_update": datetime.now(),
                "pledge": None,
                "reports_week": [],
                "last_week_report": [],
                "total_reports": 0,
                "exp_track": [],
                "gear": None,
                "gear_info": None,
                "stock": None,
                "squad": None,
                "profile": hero["profile"]
            }
            return self.heros.insert_one(thero)

    def insert_gear(self, userid, username, gear):
        return self.heros.find_one_and_update({"_id": userid}, {"$set": {
            "last_update_gear": datetime.now(),
            "gear": gear["gear"],
            "gear_info": gear["gearInfo"]
        }})

    def update_gear(self, userid):
        import SharkTeethCastleBot.services as services
        h = self.heros.find_one({"_id": userid})
        now = datetime.now()
        cw = services.CwApiService.getInstance()
        if h and "last_update_gear" in h.keys():
            last = h["last_update_gear"]
            if (now - last).seconds / 60 > 1:
                gear = cw.requestGearInfo(userid)
                if gear != "FAIL" and gear is not None:
                    print(gear)
                    self.heros.update_one({"_id": userid}, {"$set": {
                        "last_update_gear": now,
                        "gear": gear["gear"],
                        "gear_info": gear["gearInfo"]
                    }})
                    return "gear_updated"
                else:
                    return "gear_not_auth"
            else:
                return "gear_already_updated"
        else:
            return "gear_not_auth"

    def update_hero(self, userid, username=None):
        import SharkTeethCastleBot.services as services
        h = self.heros.find_one({"_id": userid})
        now = datetime.now()
        cw = services.CwApiService.getInstance()
        if h:
            last = h["last_update"]
            if (now - last).seconds / 60 > 1:
                profile = cw.requestProfile(userid)
                if profile and username:
                    response = self.heros.find_one_and_update({"_id": userid}, {"$set": {
                        "profile": profile["profile"],
                        "last_update": now,
                        "username": username
                    }})
                    return "hero_updated"
                elif profile:
                    response = self.heros.find_one_and_update({"_id": userid}, {"$set": {
                        "profile": profile["profile"],
                        "last_update": now
                    }})
                    return "hero_updated"
                else:
                    return None
            else:
                return "hero_already_updated"

    def add_to_squad(self, userid, squadshort):
        squad = self.squad.find_one({"short": squadshort})
        self.heros.update({"_id": userid}, {"$set": {"squad": {"_id": squad["_id"], "name": squad["name"]}}})

    def update_lang(self, user, lang):
        if self.herosettings.find_one_and_update({"_id": user}, {"$set": {"LANG": lang}}):
            self.lang_cache[user] = lang

    def update_many(self, query, values):
        self.heros.update_many(query, values)

    def get_lang(self, nid):
        if nid in self.lang_cache.keys():
            return self.lang_cache[nid]

        h = self.herosettings.find_one({"_id": nid}, {"LANG": 1})
        if h:
            self.lang_cache[nid] = h["LANG"]
            return self.lang_cache[nid]
        else:
            self.herosettings.update_one({"_id": nid}, {"$set": {"LANG": "EN"}})
            self.lang_cache[nid] = "EN"
            return "EN"
