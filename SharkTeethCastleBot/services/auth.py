from .dbmanager import DatabaseService
from .telegram import TelegramService
import logging

logger = logging.getLogger("[auth_service]")

class AuthService:
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if AuthService.__instance == None:
            AuthService()
        return AuthService.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if AuthService.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            AuthService.__instance = self
            self.db = DatabaseService.get_instance()
            self.permissions = self.db.permissions
            
    def get_role(self, userid):
        if self.db.is_hero_auth(userid):
            roles = self.permissions.find().sort("priority", 1)
            for role in roles:
                if role["_id"] == Permissions.COMMANDER and userid in role["list"]:
                    return (Permissions.COMMANDER, None)
                if role["_id"] == Permissions.SQUAD_LEADER or role["_id"] == Permissions.GUILD_LEADER:
                    if str(userid) in role["list"].keys():
                       return (role["_id"], role["list"][str(userid)])
                if role["_id"] == Permissions.MODERATOR and role["list"] and str(userid) in role["list"]:
                    return (Permissions.MODERATOR, None)        
                    
            return (Permissions.SOLDIER, None)
        else:
            return (Permissions.NO_AUTH, None)
        
    def can_create_squad(self, userId):
        permissions = DatabaseService.get_instance().permissions
        commander = permissions.find_one({"_id": Permissions.COMMANDER}, {"list"})["list"]
        return userId in commander
    
    def can_add_to_squad(self, comm, squadId):
        permissions = DatabaseService.get_instance().permissions
        commanders = permissions.find({
            "_id": {
                "$in": [Permissions.COMMANDER, Permissions.SQUAD_LEADER]} 
            }).sort("priority", 1 )
        for commander in commanders:
            if commander["_id"] == Permissions.COMMANDER and comm in commander["list"]:
                return True
            if commander["_id"] == Permissions.SQUAD_LEADER \
                and str(comm) in commander["list"].keys() and commander["list"][str(comm)] == squadId:
                return True
        return False

    def can_see_profile(self, userid, commanderid):
        heros = self.db.heros
        permissions = self.db.permissions
        h = heros.find_one({"_id":userid})
        ts = TelegramService.get_instance()
        if h:
            commander = permissions.find({
            "_id": {
                "$in": [Permissions.COMMANDER, Permissions.SQUAD_LEADER, Permissions.GUILD_LEADER]} 
            }).sort("priority", 1)
            
            if commander == None:
                return False 
            
            squadId = h["squad"]["_id"] if h["squad"] is not None else None
            guild = h["profile"]["guild_tag"] if "guild_tag" in h["profile"].keys() else None
            
            for i in commander:
                if i["_id"] == Permissions.COMMANDER and commanderid in i["list"]:
                    return True
                elif i["_id"] != Permissions.COMMANDER:
                    commanderid = str(commanderid)
                    if i["_id"] == Permissions.SQUAD_LEADER and \
                        commanderid in i["list"].keys() and i["list"][commanderid] == squadId:
                                return True
                    print
                    if i["_id"] == Permissions.GUILD_LEADER and \
                        commanderid in i["list"].keys() and i["list"][commanderid] == guild:
                                return True
            return False
        else:
            return False
    
class Permissions:
    DEVELOPER = "DEVELOPER"
    COMMANDER = "COMMANDERS"
    SQUAD_LEADER = "SQUAD_LEADER"
    GUILD_LEADER = "GUILD_LEADER"
    SOLDIER = "SOLDIER"
    MODERATOR = "MODERATOR"
    NO_AUTH = "NO_AUTH"