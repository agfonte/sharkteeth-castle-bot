import os, threading, pika, json, logging, time, SharkTeethCastleBot.services
from ..settings import Settings
from pika.exceptions import ChannelWrongStateError

logger = logging.getLogger("[cwapi_service]")
logging.basicConfig(level=logging.INFO)


class CwApiService:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CwApiService.__instance is None:
            CwApiService()
        return CwApiService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CwApiService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CwApiService.__instance = self
            self.settings = Settings.get_instance()
            self.db = SharkTeethCastleBot.services.DatabaseService.get_instance()
            self.actions = SharkTeethCastleBot.services.ActionService.get_instance()
            self.cwuser = self.settings.cwuser
            self.cwpass = self.settings.cwpass
            self.url = "amqps://" + self.cwuser + ":" + self.cwpass + "@api.chatwars.me:5673/"
            self.connection = None
            self.parameters = None
            self.threadLock = threading.Lock()
            self.channel = None
            self.init_connection()

    def init_connection(self):
        self.threadLock.acquire()
        self.parameters = pika.connection.URLParameters(self.url)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.empty_queue()
        self.threadLock.release()

    def empty_queue(self):
        no_response = True
        while no_response:
            method_frame, header_frame, body = self.channel.basic_get(f"{self.cwuser}_i")
            if method_frame:
                response = json.loads(body)
                self.channel.basic_ack(method_frame.delivery_tag)
                logging.info("Empting queue - Consumed action:" + response["action"])
            else:
                no_response = False
        print("Queue Empty")

    def consume_from_api(self):
        no_response = True
        while no_response:
            method_frame, header_frame, body = self.channel.basic_get(f"{self.cwuser}_i")
            if method_frame:
                response = json.loads(body)
                self.channel.basic_ack(method_frame.delivery_tag)
                no_response = False
                logging.info("Consumed action:" + response["action"])
                return self.actions.resolve(response)

    def send_message_api(self, message):
        sent = False
        self.threadLock.acquire()
        while not sent:
            try:
                self.channel.basic_publish(exchange=f"{self.cwuser}_ex", routing_key=f"{self.cwuser}_o",
                                           body=json.dumps(message))
                sent = True
            except:
                self.connection.close()
                self.threadLock.release()
                self.init_connection()
                logging.error("ERROR PUBLISHING TO API: ", exc_info=True)
        try:
            response = self.consume_from_api()
            sent = True
            self.threadLock.release()
            return response
        except ChannelWrongStateError as err:
            logging.error(err)
            self.connection.close()
            self.threadLock.release()
            self.init_connection()
        except Exception:
            logging.error("ERROR CONSUMING FROM API", exc_info=True)
            self.connection.close()
            self.threadLock.release()
            self.init_connection()
        return "FAIL"

    def auth(self, userid):
        return self.send_message_api({"action": "createAuthCode",
                                      "payload": {
                                          "userId": userid
                                      }
                                      })

    def grant_token(self, userid, code):
        return self.send_message_api({"action": "grantToken",
                                      "payload": {
                                          "userId": userid,
                                          "authCode": code
                                      }
                                      })

    def auth_gear(self, userid):
        return self.auth_additional_operation(userid, "requestGearInfo")

    def request_profile(self, userid):
        token = self.db.get_token_by_user(userid)
        response = self.send_message_api({"token": token,
                                          "action": "requestProfile"
                                          })
        return response

    def auth_request_gear_info(self, userid):
        token = self.db.get_token_by_user(userid)
        return self.auth_additional_operation(userid, token, "GetGearInfo")

    def grant_additional_operation(self, userid, code):
        token = self.db.get_token_by_user(userid)
        request_id = self.db.auth.find_one({"_id": userid}, {"uuid": 1})
        response = None
        if request_id and request_id["uuid"]:
            response = self.send_message_api(
                {
                    "token": token,
                    "action": "grantAdditionalOperation",
                    "payload": {
                        "requestId": request_id["uuid"],
                        "authCode": code
                    }
                }
            )
        return response

    def auth_additional_operation(self, userid, token, operation):
        action = {
            "token": token,
            "action": "authAdditionalOperation",
            "payload": {
                "operation": operation
            }
        }
        return self.send_message_api(action)

    def request_gear_info(self, userid):
        action = {
            "token": self.db.get_token_by_user(userid),
            "action": "requestGearInfo"
        }
        return self.send_message_api(action)
