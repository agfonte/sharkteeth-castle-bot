from ..keyboard.botmarkup import gen_lang_settings, \
    gen_main_keyboard
from ..services import DatabaseService, LanguageService, TelegramService


class Settings:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Settings.__instance is None:
            Settings()
        return Settings.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Settings.__instance = self
            self.db = DatabaseService.get_instance()
            self.lang = LanguageService().get_instance()
            self.cwuser = None
            self.cwpass = None
            self.telegram = TelegramService.get_instance()

    def select_language(self, userid):
        self.telegram.send_message(userid, "select_lang", reply_markup=gen_lang_settings(),
                                   parse_mode="Markdown")

    def proccess_callback(self, call):
        heros = self.db.herosettings
        user = call.from_user.id
        lang = call.data.split("LANG_")[1]
        ts = TelegramService.get_instance()
        self.telegram.bot.answer_callback_query(call.id, "Ok")
        self.db.update_lang(user, lang)
        if lang == "ES":
            ts.send_message(user, text="lang_setted", reply_markup=gen_main_keyboard(user))
        elif lang == "EN":
            ts.send_message(user, text="lang_setted", reply_markup=gen_main_keyboard(user))

    def set_env(self, user, passw):
        self.cwuser = user
        self.cwpass = passw
