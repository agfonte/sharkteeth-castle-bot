from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from SharkTeethCastleBot.utils.constants import buttons, emojis


def lang_index(userid):
    import SharkTeethCastleBot.services as services
    lang = services.LanguageService.get_instance()
    return 0 if lang.get_lang(userid) == "EN" else 1


def gen_main_keyboard(userid):
    import SharkTeethCastleBot.services as services
    auth = services.AuthService.get_instance().get_role(userid)
    print("Keyboard " + auth[0])
    if auth is None:
        return None
    if auth[0] == services.Permissions.COMMANDER:
        return gen_main_commander_keyboard(userid)
    if auth[0] == services.Permissions.SQUAD_LEADER:
        return gen_main_squad_commander_keyboard(userid)
    if auth[0] == services.Permissions.GUILD_LEADER:
        return gen_main_guild_leader_keyboard(userid)
    if auth[0] == services.Permissions.SOLDIER:
        return gen_main_soldier_keyboard(userid)
    if auth[0] == services.Permissions.NO_AUTH:
        return None


def gen_hero_markup(userid):
    import SharkTeethCastleBot.services as services
    hero = services.DatabaseService.get_instance().heros.find_one({"_id": userid}, {"squad": 1})
    markup = InlineKeyboardMarkup()

    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🏅🔄", callback_data="HERO_UPDATE"),
        InlineKeyboardButton("🎽🔄", callback_data="HERO_GEAR_UPDATE")
    )
    if hero["squad"]:
        markup.add(
            InlineKeyboardButton("Quit squad", callback_data="QUIT_SQUAD")
        )
    return markup


def gen_whois_markup(userid, commanderid):
    import SharkTeethCastleBot.services as services
    hero = services.DatabaseService.get_instance().heros.find_one({"_id": userid}, {"squad": 1})
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🏅🔄", callback_data="HERO_UPDATE_" + str(userid)),
        InlineKeyboardButton("🎽🔄", callback_data="HERO_GEAR_UPDATE_" + str(userid))
    )
    role = services.AuthService.get_instance().get_role(commanderid)

    if hero["squad"]:
        txt = "Change Squad"
        if role[0] == "COMMANDERS":
            markup.add(
                InlineKeyboardButton(txt, callback_data="ADD_SQUAD_ID_" + str(userid)),
                InlineKeyboardButton("Remove from Squad", callback_data="DEL_SQUAD_ID_" + str(userid))
            )
        if role[0] == "SQUAD_LEADER" and role[1] == hero["squad"]["_id"]:
            markup.add(InlineKeyboardButton("Remove from Squad", callback_data="DEL_SQUAD_ID_" + str(userid)))
    else:
        txt = "Add Squad"
        if role[0] == "SQUAD_LEADER" and not hero["squad"]:
            markup.add(InlineKeyboardButton(txt, callback_data="ADD_SQUAD_ID_" + str(userid)))
        elif role[0] == "COMMANDERS":
            markup.add(
                InlineKeyboardButton(txt, callback_data="ADD_SQUAD_ID_" + str(userid)),
                InlineKeyboardButton("Remove from Squad", callback_data="DEL_SQUAD_ID_" + str(userid))
            )
    return markup


def gen_markup(fight, text):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(text, callback_data=fight))
    return markup


def gen_lang_settings():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🇪🇸Español", callback_data="LANG_ES"),
               InlineKeyboardButton("🇬🇧English", callback_data="LANG_EN"))
    return markup


def gen_bot_settings(userid):
    index = lang_index(userid)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    lang = KeyboardButton(buttons["lang"][index])
    settings = KeyboardButton(buttons["other_settings"][index])
    back = KeyboardButton(buttons["back"][index])
    markup.row(lang, settings, back)
    return markup


def gen_main_soldier_keyboard(userid):
    index = lang_index(userid)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    me = KeyboardButton(buttons["me"][index])
    mysquad = KeyboardButton(buttons["mysquad"][index])
    tops = KeyboardButton(buttons["tops"][index])
    settings = KeyboardButton(buttons["settings"][index])
    shops = KeyboardButton(buttons["shops"][index])
    faq = KeyboardButton(buttons["faq"][index])
    markup.row(me, mysquad, tops)
    markup.row(settings, shops, faq)
    return markup


def gen_main_squad_commander_keyboard(userid):
    index = lang_index(userid)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    me = KeyboardButton(buttons["me"][index])
    mysquad = KeyboardButton(buttons["mysquad"][index])
    tops = KeyboardButton(buttons["tops"][index])
    settings = KeyboardButton(buttons["settings"][index])
    shops = KeyboardButton(buttons["shops"][index])
    faq = KeyboardButton(buttons["faq"][index])
    markup.row(me, mysquad, tops)
    markup.row(settings, shops, faq)
    return markup


def gen_main_guild_leader_keyboard(userid):
    index = lang_index(userid)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    me = KeyboardButton(buttons["me"][index])
    mysquad = KeyboardButton(buttons["mysquad"][index])
    tops = KeyboardButton(buttons["tops"][index])
    settings = KeyboardButton(buttons["settings"][index])
    shops = KeyboardButton(buttons["shops"][index])
    faq = KeyboardButton(buttons["faq"][index])
    markup.row(me, mysquad, tops)
    markup.row(settings, shops, faq)
    return markup


def gen_main_commander_keyboard(userid):
    index = lang_index(userid)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    me = KeyboardButton(buttons["me"][index])
    mysquad = KeyboardButton(buttons["mysquad"][index])
    guild = KeyboardButton(buttons["guild"][index])

    tops = KeyboardButton(buttons["tops"][index])
    shops = KeyboardButton(buttons["shops"][index])

    orders = KeyboardButton(buttons["orders"][index])
    squads = KeyboardButton(buttons["squads"][index])
    admin = KeyboardButton(buttons["admin"][index])

    settings = KeyboardButton(buttons["settings"][index])
    faq = KeyboardButton(buttons["faq"][index])

    markup.row(me, mysquad, guild)
    markup.row(tops, shops)
    markup.row(orders, squads, admin)
    markup.row(settings, faq)
    return markup


def gen_add_to_squad(userid, list_squad):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for i in list_squad:
        markup.add(InlineKeyboardButton(i[0], callback_data="SELECT_SQUAD_" + str(i[1]) + "_" + str(userid)))
    return markup


def gen_confirm_markup(userid):
    import SharkTeethCastleBot.services as services
    lang = services.LanguageService.get_instance()
    yes = lang.get_value(userid, "confirm_yes")
    no = lang.get_value(userid, "confirm_no")
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(yes, callback_data="QUIT_SQUAD_CONFIRM_YES"),
               InlineKeyboardButton(no, callback_data="QUIT_SQUAD_CONFIRM_NO")
               )
    return markup


def gen_tops_keyboard(userid):
    import SharkTeethCastleBot.services as services
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    atk = KeyboardButton(emojis["cross_swords"])
    defense = KeyboardButton(emojis["shield"])
    exp = KeyboardButton(emojis["fire"])
    reports = KeyboardButton(emojis["star_medal"])
    back = KeyboardButton(emojis["left_arrow"] + services.LanguageService.get_instance().get_value(userid, "back"))
    markup.row(atk, defense, exp)
    markup.row(reports, back)
    return markup
