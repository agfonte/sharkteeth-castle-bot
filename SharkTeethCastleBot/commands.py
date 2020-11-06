

@bot.message_handler(commands=['hunt'])
def hunt(message):
    hunting.hunt(message)
    
@bot.message_handler(commands=['setminlvl'])
def setminlvl(message):
    hunting.setminlvl(message)
            
@bot.message_handler(commands=['setmaxlvl'])
def start(message):
    hunting.setmaxlvl(message)

@bot.message_handler(commands=['sethelpmaxlvl'])
def setallowmaxlvl(message):
    hunting.setallowmaxlvl(message)

@bot.message_handler(commands=['sethelpminlvl'])
def setallowminlvl(message):
    hunting.setallowminlvl(message)


@bot.message_handler(commands=['mystats'])
def mystats(message):
    hunting.mystats(message)
    
@bot.message_handler(commands=['stop'])
def stop(message):
    hunting.stop(message)

@bot.message_handler(commands=['help'])
def help(message):
    lng = lang.get_value(message.from_user.id, "helpmsg")
    bot.send_message(message.from_user.id, lng)

@bot.message_handler(commands=['tutorial'])
def tutorial(message):
    lng = lang.get_value(message.from_user.id, "tutorialmsg")
    bot.send_message(message.from_user.id, lng)


@bot.message_handler(func=lambda m: m.text in lang.command_buttons(m))
def buttons_actions(message):
    text = message.text
    meicon, hunticon, stopicon, statsicon,settingicon = lang.command_buttons(message)
    if text == meicon:
        mystats(message)
    elif text == hunticon:
        hunt(message)
    elif text == stopicon:
        stop(message)
    elif text == statsicon:
        stats.top_hunters(message.from_user.id)
    elif text == settingicon:
        settings.language(message)
    else:
        bot.send_message(message.from_user.id, "This message is not supported.")

    
@bot.message_handler(func=lambda m: True)
def update(message):
    if message.chat.type == "private" \
        and message.forward_from is not None \
            and message.forward_from.id == chatWarsBotId:
        if hero.parse_hero(message):
            return
        if hunting.parse_mob(message):
            return
        if hunting.parse_preparing(message):
            return
        if hunting.parse_too_late(message):
            return

    else:
        bot.send_message(message.from_user.id, "This message is not forwarded from @chtwrsbot.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("/fight_"))
def fight_callback_query(call):
    hunting.callback_hunt(call)
        
@bot.callback_query_handler(func=lambda call: call.data.startswith("LANG_"))
def fight_callback_query(call):
    settings.callback_language(call)

