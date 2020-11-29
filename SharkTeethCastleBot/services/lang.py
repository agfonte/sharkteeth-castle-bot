from SharkTeethCastleBot.services import DatabaseService
import logging
from SharkTeethCastleBot.languages import strings_en, strings_es

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[language_service]")


class LanguageService:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if LanguageService.__instance is None:
            LanguageService()
        return LanguageService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if LanguageService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LanguageService.__instance = self
            self.es = strings_es.lang_es
            self.en = strings_en.lang_en
            self.db = DatabaseService.get_instance()

    def get_lang(self, userid):
        return self.db.get_lang(userid)

    def get_value(self, _id, msg):
        print(msg)
        lang = self.db.get_lang(_id)
        if lang == "ES":
            return self.es[msg]
        elif lang == "EN":
            return self.en[msg]

    def command_buttons(self, msg):
        user_id = msg.from_user.id
        lang = self.db.get_lang(user_id)
        buttons = self.en
        logging.info("User[" + str(user_id) + "] with lang: " + str(lang))
        if lang == "ES":
            buttons = self.es

        return [buttons["meicon"],
                buttons["hunticon"],
                buttons["stopicon"],
                buttons["statsicon"],
                buttons["settingicon"]]
