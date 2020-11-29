from SharkTeethCastleBot.utils.constants import commands, buttons
import re
from SharkTeethCastleBot.services import LanguageService


def parse_code_auth(txt):
    x = re.match("Code [0-9][0-9][0-9][0-9][0-9][0-9] to authorize", txt)
    if x:
        code = re.search("[0-9][0-9][0-9][0-9][0-9][0-9]", txt)
        print(code.group())
        return code.group()


def is_command(message):
    if message.content_type == "text":
        for i in commands.values():
            if message.text.startswith(i):
                return i
    return None


def split_command(text, com):
    res = text.split(com)
    return res[0].strip(), res[1].strip()


def all_buttons(userid):
    index = 0 if LanguageService.get_instance().get_lang(userid) == "EN" else 1
    lang_buttons = {}
    for key, value in buttons.items():
        lang_buttons[key] = value[index]
    return lang_buttons


def is_battle_report(text):
    return "Your result on the battlefield:" in text


def check_if_pledge(text):
    if "You were invited by the knight of" in text and "Choose the castle you will pledge your allegiance to 🗡" in text:
        return text.split("You were invited by the knight of the ")[1].strip().split(
            "Choose the castle you will pledge your allegiance to 🗡")[0].strip()


def emoji_to_class(emoji):
    classes = {
        "⚔️": "Knight",
        "🛡": "Sentinel",
        "🏹": "Ranger",
        "⚗️": "Alchemist",
        "⚒": "Blacksmith",
        "📦": "Collector",
        "🐣": "Warrior"
    }
    return classes[emoji]


def correspondent_utc(hour):
    first_battle = 7
    second_battle = 15
    third_battle = 23
    if first_battle < hour < second_battle:
        return 7
    elif second_battle < hour < third_battle:
        return 15
    elif third_battle < hour < first_battle:
        return 23


def quality_to_letter(quality):
    if "Masterpiece" in quality:
        return "A" if "Epic" not in quality else "SA"
    elif "Excellent" in quality:
        return "B" if "Epic" not in quality else "SB"
    elif "Great" in quality:
        return "C" if "Epic" not in quality else "SC"
    elif "High" in quality:
        return "D" if "Epic" not in quality else "SD"
    elif "Fine" in quality:
        return "E" if "Epic" not in quality else "SE"
    elif "Common" in quality:
        return ""
