import logging

from .auth import AuthService
from .dbmanager import DatabaseService
from .telegram import TelegramService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[database]")


class SquadManagementService:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if SquadManagementService.__instance is None:
            SquadManagementService()
        return SquadManagementService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SquadManagementService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SquadManagementService.__instance = self
            self.db = DatabaseService.get_instance()
            self.squad = self.db.squad
            self.permissions = self.db.permissions
            self.auth = AuthService.get_instance()
            self.ts = TelegramService.get_instance()
            self.heros = self.db.heros

    def squad_info(self, squadid):
        return self.squad.find_one({"_id": squadid})

    def add_player(self, _id, squadid):
        h = self.db.heros.find_one({"_id": _id})
        if h:
            self.squad.insert_one({"_id"})

    def create_squad(self, message, comm):
        msg = message.text
        commander_username = message.from_user.username
        commander_id = message.from_user.id
        squad_id = message.chat.id

        if not self.auth.can_create_squad(commander_id):
            return self.ts.send_message(squad_id, "cant_create_squad", user_id=commander_id)

        squadname = msg.lstrip(comm + " ")
        res = squadname.split(",")

        if len(res) != 2:
            self.ts.send_message(message.chat.id, "squad_create_incorrect_parameters", user_id=commander_id)

        squadname = res[0]
        squadshort = res[1]

        userId = message.from_user.id
        chatId = message.chat.id

        h = self.squad.find_one({"_id": squad_id}, {"name": 1, "short": 1})
        if h is None:
            commander = message.from_user.username
            if not commander:
                commander = message.from_user.first_name
            else:
                commander = "@" + str(commander)
            if not self.squad.find_one({"short": squadshort}):
                self.ts.export_chat_invite_link(squad_id)
                link = self.ts.get_chat(squad_id).invite_link
                if not link:
                    return self.ts.send_message(message.chat.id, "squad_create_incorrect_parameters",
                                                user_id=commander_id)
                self.squad.insert_one({
                    "_id": squad_id,
                    "name": squadname,
                    "short": squadshort.upper(),
                    "link": link,
                    "commander": None,
                    "squad": True
                })
                return self.ts.send_message(squad_id, "squad_created", user_id=commander_id,
                                            params=(squadname, squadshort, commander))
            else:
                return self.ts.send_message(squad_id, "squad_exists", user_id=commander_id, params=(squad_id, h["name"]))
        else:
            self.ts.send_message(squad_id, "squad_exists", user_id=commander_id, params=(squad_id, h["name"]))

    def delete_squad(self, message, comm):
        commander_username = message.from_user.username
        commander_id = message.from_user.id
        squad_id = message.chat.id

        if not self.auth.can_create_squad(commander_id):
            return self.ts.send_message(squad_id, "cant_delete_squad", user_id=commander_id)

        user_id = message.from_user.id
        chat_id = message.chat.id

        h = self.squad.find_one({"_id": squad_id}, {"name": 1, "short": 1})
        if h is None:
            commander = message.from_user.username
            squadname = h['name']
            squadshort = h['short']
            if not commander:
                commander = message.from_user.first_name
            else:
                commander = "@" + str(commander)
            self.squad.delete_one({
                "_id": squad_id
            })
            return self.ts.send_message(squad_id, "squad_deleted", user_id=commander_id,
                                        params=(squadname, squadshort, commander))
        else:
            self.ts.send_message(squad_id, "squad_no_exists", user_id=commander_id, params=(squad_id, h["name"]))

    def can_enter(self, userid, squadid):
        hero = self.heros.find_one({"_id": userid})
        if hero and hero["squad"] and hero["squad"]["_id"] == squadid:
            return True
        else:
            return False

    def add_private_to_squad(self, message):
        params = message.text.split("/add")[1].strip()
        params = params.split(" ")
        if len(params) > 2:
            return self.ts.reply_to(message, "bad_params_add")
        username = params[0].strip()
        squad = params[1].strip().upper()
        if "@" in username:
            username = username.split("@")[1]
            username = DatabaseService.get_instance().heros.find_one({"username": username}, {"_id": 1})["_id"]
        if self.auth.can_add_to_squad(message.from_user.id, squad):
            DatabaseService.get_instance().add_to_squad(username, squad)

    def add_to_squad_by_join(self, message):
        if message.reply_to_message.content_type != "new_chat_members":
            return self.ts.reply_to(message, "add_no_join")

        if self.auth.can_add_to_squad(message.from_user.id, message.reply_to_message.chat.id):
            DatabaseService.get_instance().add_to_squad(message.reply_to_message.from_user.id,
                                                        message.reply_to_message.chat.id)
