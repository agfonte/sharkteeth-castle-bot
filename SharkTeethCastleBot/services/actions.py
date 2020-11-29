import logging
from SharkTeethCastleBot.services import DatabaseService, TelegramService


class ActionService:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if ActionService.__instance is None:
            ActionService()
        return ActionService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ActionService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ActionService.__instance = self
            self.db = DatabaseService.get_instance()
            self.bot = TelegramService.get_instance()
            self.OK = "Ok"

    def resolve(self, response):
        action = response["action"]
        result = response["result"]
        payload = response["payload"]
        if action == "createAuthCode":
            return self.action_create_auth_code(result, payload)
        if action == "grantToken":
            return self.action_grant_token(result, payload)
        if action == "authAdditionalOperation":
            return self.action_auth_additional_operation(response)
        if action == "grantAdditionalOperation":
            return self.action_grant_additional_operation(result, payload)
        if action == "viewCraftbook":
            return self.action_view_craftbook(result, payload)
        if action == "requestProfile":
            res = self.action_request_profile(result, payload)
            return res
        if action == "requestBasicInfo":
            return self.action_request_basic_info(result, payload)
        if action == "requestGearInfo":
            return self.action_request_gear_info(result, payload)
        if action == "requestStock":
            return self.action_request_stock(result, payload)
        if action == "guildInfo":
            return self.action_guild_info(result, payload)
        if action == "wantToBuy":
            return self.action_want_to_buy(result, payload)

    def action_create_auth_code(self, result, payload):
        return result

    def action_grant_token(self, result, payload):
        if result == self.OK:
            try:
                self.db.insert_authed_user(payload["userId"], payload["id"], payload["token"])
                logging.info("Inserted: " + str(payload["userId"]))
            except:
                logging.error("Error in: action_grant_token with params(" + str(payload) + ")")
        else:
            userid = payload["userId"]
            self.bot.send_message(userid, "invalid_token")
        return result

    def action_auth_additional_operation(self, response):
        result = response["result"]
        payload = response["payload"]
        if result == self.OK:
            auth = self.db.auth
            auth.update({"_id": payload["userId"]}, {"$set": {
                "uuid": response["uuid"]
            }})
        return result

    def action_grant_additional_operation(self, result, payload):
        if result == self.OK:
            print(result, payload)
            logging.info("Updated token for: " + str(payload))
        else:
            userid = payload["userId"]
            self.bot.send_message(userid, "invalid_token")
        return result

    def action_view_craftbook(self, result, payload):
        return result

    def action_request_profile(self, result, payload):
        if result == self.OK:
            return payload
        else:
            userid = payload["userId"]
            self.bot.send_message(userid, "invalid_token")

    def action_request_basic_info(self, result, payload):
        print(result, payload)

    def action_request_gear_info(self, result, payload):
        if result == self.OK:
            return payload
        else:
            userid = payload["userId"]
            self.bot.send_message(userid, "no_gear_auth")

    def action_request_stock(self, result, payload):
        print(result, payload)

    def action_guild_info(self, result, payload):
        print(result, payload)

    def action_want_to_buy(self, result, payload):
        print(result, payload)
