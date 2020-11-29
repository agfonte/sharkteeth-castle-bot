from SharkTeethCastleBot.services import DatabaseService, LanguageService, TelegramService
from SharkTeethCastleBot.keyboard.botmarkup import gen_bot_settings, gen_main_soldier_keyboard, gen_lang_settings, \
    gen_main_keyboard


class Settings:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Settings.__instance == None:
            Settings(bot, lang_service)
        return Settings.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Settings.__instance = self
            self.db = DatabaseService.get_instance()
            self.lang = LanguageService().getInstance()
            self.cwuser = None
            self.cwpass = None

    def select_language(self, userid):
        TelegramService.get_instance().send_message(userid, "select_lang", reply_markup=gen_lang_settings(),
                                                    parse_mode="Markdown")

    def proccess_callback(self, call):
        heros = self.db.herosettings
        user = call.from_user.id
        lang = call.data.split("LANG_")[1]
        ts = TelegramService.get_instance()
        ts.bot.answer_callback_query(call.id, "Ok")
        self.db.update_lang(user, lang)
        if lang == "ES":
            ts.send_message(user, text="lang_setted", reply_markup=gen_main_keyboard(user))
        elif lang == "EN":
            ts.send_message(user, text="lang_setted", reply_markup=gen_main_keyboard(user))

    def setEnv(self, user, passw):
        self.cwuser = user
        self.cwpass = passw
