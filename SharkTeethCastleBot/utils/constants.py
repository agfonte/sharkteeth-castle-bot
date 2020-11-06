buttons = {
    "me": ("🏅Hero", "🏅Heroe"),
    "mysquad": ("📯My Squad", "📯My Escuadrón"),
    "tops": ("⭐️Tops", "⭐️Mejores Players"),
    "settings" : ("⚙️Settings", "⚙️Ajustes"),
    "shops": ("🎪Shops", "🎪Tiendas"),
    "faq": ("📖FAQ", "📖FAQ"),
    "orders": ("⚔️🛡 Orders", "⚔️🛡Órdenes"),
    "squads": ("📯Castle Squads", "📯Escuadrones del Castillo"),
    "admin" : ("🔐Administration", "🔐Administración"),
    "guild" : ("👥Guild", "👥Gremio"),
    "top_atk": ("⚔️", "⚔️"),
    "top_def": ("🛡", "🛡"),
    "top_exp": ("🔥", "🔥"),
    "top_report": ("🎖", "🎖"),
    "top_atk_squad": ("⚔️", "⚔️"),
    "top_def_squad": ("🛡", "🛡"),
    "top_exp_squad": ("🔥", "🔥"),
    "top_report_squad": ("🎖", "🎖"),
    "back": ("⬅Back", "⬅Atrás"),
    "lang": ("🇬🇧Language", "🇪🇸Idioma"),
    "other_settings": ("⚙️Other settings", "⚙️Otros ajustes")
}



commands= {
    "first_steps": "/first_steps",
    "no_pledge" : "/no_pledge",
    "start": "/start", 
    "hunt" : "/hunt", 
    "stop": "/stop", 
    "help": "/help",
    "mystats": "/mystats", 
    "setminlvl":"/setminlvl", 
    "setmaxlvl": "/setmaxlvl", 
    "sethelpmaxlvl": "/sethelpmaxlvl",
    "sethelpminlvl": "/sethelpminlvl", 
    "sethelpminlvl": "/sethelpminlvl", 
    "sethelpminlvl": "/sethelpminlvl",
    "auth": "/auth",
    "gearAuth": "/gearAuth",
    "create_squad": "/create_squad",
    "profile": "/profile",
    "add_squad": "/add",
    "whois": "/whois",
    "kick": "/kick",
    "ban": "/ban",
    "unban": "/unban",
    "reports": "/reports",
    "add": "/add"
}

private_commands = {
    "first_steps": "/first_steps",
    "no_pledge" : "/no_pledge",
    "start": "/start", 
    "hunt" : "/hunt", 
    "stop": "/stop", 
    "help": "/help",
    "mystats": "/mystats", 
    "setminlvl":"/setminlvl", 
    "setmaxlvl": "/setmaxlvl", 
    "sethelpmaxlvl": "/sethelpmaxlvl",
    "sethelpminlvl": "/sethelpminlvl", 
    "sethelpminlvl": "/sethelpminlvl", 
    "sethelpminlvl": "/sethelpminlvl",
    "auth": "/auth",
    "gearAuth": "/gearAuth",
    "profile": "/profile",
    "reports": "/reports",
    "add": "/add",
    "whois": "/whois",
}

public_commands = {
    "auth": "/auth",
    "create_squad": "/create_squad",
    "delete_squad": "/delete_squad",
    "squad_name": "/squad_name",
    "profile": "/profile",
    "add": "/add",
    "kick": "/kick",
    "ban": "/ban",
    "unban": "/unban",
    "add": "/add",
    "whois": "/whois"
}


preparing= "You are preparing for a fight"

too_late = "Too late. Action is not available."

encounter = "👾Encounter:"

chatWarsBotId = 408101137


from datetime import timedelta
threshold = timedelta(microseconds=450000)

castle = '🦈'

level = '🏅'

share_url = "https://t.me/share/url?url="
        
        
heroscheme = { 
            "name": "", 
            "guild": None, ""
            "lvl": 0 , 
            "_id": -1,
            "maxlvl": 10,
            "minlvl": 10,
            "allowmaxlvl": 10,
            "allowminlvl":10,
            "too_late":0,
            "preparing": 0,
            "hunting": False,
            "last_mob": None,
            "LANG":"EN"
            }
scripter = {
            "_id" : -1,
            "times_detected":0,
            "last": None
            }
modificator = "╰ "

text_to_emoji= {
    "bear": "🐻",
    "boar": "🐗",
    "wolf": "🐺",
    "knight": "⚔️",
    "sentinel": "🛡",
    "ranger": "🏹",
    "alchemist": "⚗️",
    "blacksmith": "⚒",
    "collector": "📦",
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
}

emojis = {
    "cross_swords": "⚔️",
    "shield": "🛡",
    "bow": "🏹",
    "alambique": "⚗️",
    "cross_hammer": "⚒",
    "box": "📦",
    "heart": "❤️",
    "gold": "💰",
    "pog": "👝",
    "fire": "🔥",
    "stamina": "🔋",
    "equipment": "🎽",
    "lightning": "⚡️",
    "id":"🆔",
    "shark": "🦈",
    "moon": "🌑",
    "wolf": "🐺",
    "deer": "🦌",
    "potato":"🥔",
    "eagle":"🦅",
    "dragon": "🐉",
    "guild" : "👥",
    "rounded_medal" : "🏅",
    "star_medal": "🎖",
    "horn": "📯",
    "star": "⭐️",
    "bright_star": "🌟",
    "diamond": "💎",
    "bag": "🎒",
    "soon_arrow": "🔜",
    "left_arrow": "⬅️",
    "settings": "⚙️",
    "shop": "🎪",
    "open_book": "📖"
}


levels = {
        1:5, 
        2:15,
        3:38,
        4:79,
        5:142,
        6:227,
        7:329,
        8:444,
        9:577,
        10:721,
        11:902,
        12:1127,
        13:1409,
        14:1761,
        15:2202,
        16:2752,
        17:3440,
        18:4300,
        19:5375,
        20:6719,
        21:8399,
        22:10498,
        23:13123,
        24:16404,
        25:20504,
        26:25631,
        27:32038,
        28:39023,
        29:46636,
        30:54934,
        31:63979,
        32:73838,
        33:84584,
        34:96297,
        35:109065,
        36:122982,
        37:138151,
        38:154685,
        39:172708,
        40:192353,
        41:213765,
        42:237105,
        43:262545,
        44:290275,
        45:320501,
        46:353447,
        47:389358,
        48:428501,
        49:471167,
        50:517673,
        51:568364,
        52:623618,
        53:683845,
        54:804299,
        55:935594,
        56:1077392,
        57:1229117,
        58:1389944,
        59:1663352,
        60:1961366,
        61:2283221,
        62:2627606,
        63:2992654,
        64:3540225,
        65:4137079,
        66:4781681,
        67:5471404,
        68:6202512,
        69:7226062,
        70:8341732,
        71:9546655,
        72:10835923,
        73:12202547,
        74:13979158,
        75:15915664
}


debug = "false"
try:
    debug = os.environ["DEBUG"]
except:
    print("Not DEBUG mode")


def check_time(d, maxt):
    from datetime import timedelta, datetime
    current = datetime.now()
    d  = datetime.fromtimestamp(d)
    global debug
    if debug == "true":
        return False
    else:
        return (current- d).total_seconds()/60 > maxt

