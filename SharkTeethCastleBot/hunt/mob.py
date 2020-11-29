from utils import text_to_emoji

class Mob:
    
    def __init__(self, type=None, lvl=0, amount=1, mod=None):
        super().__init__()
        self.type = type
        self.amount = amount
        self.lvl = lvl
        self.mod = mod
    
    def set_mod(self, mod):
        self.mod = mod
    
    def __str__(self):
        return f"{self.type}({self.amount})  lvl {self.lvl}, --> {self.mod}"


class Mobs:
    
    def __init__(self):
        super().__init__()
        self.mobs = []
        
    def append(self,mob):
        self.mobs.append(mob)
        
    
    def mobtext(self):
        string_mobs = ""
        for i in self.mobs:
            type_emoji = text_to_emoji[i.type.split(" ")[1].lower()]
            amount_emoji = text_to_emoji[i.amount]
            modifier = i.mod
            if modifier:
                string_mobs += f"{type_emoji} {i.type} x {amount_emoji}  <b>{i.lvl}lvl</b> ({modifier})\n"
            else:
                string_mobs += f"{type_emoji} {i.type} x {amount_emoji}  <b>{i.lvl}lvl</b>\n"
        return string_mobs