import logging

import plugins


logger = logging.getLogger(__name__)


def _initialise(bot):
    plugins.register_handler(_handle_haha_message, "message")
    plugins.register_user_command(["hahas", "scoreboard"])


def _handle_haha_message(bot, event, command):
    """handle mesages that are haha"""
    if event.text == "haha":
        logger.debug("haha message")
        last_not_haha = bot.conversation_memory_get(event.conv_id, "last_not_haha_user_id")
        if event.user_id.chat_id != last_not_haha:
            old_count = bot.user_memory_get(last_not_haha, "haha_count")
            if old_count is None:
                old_count = 0
            n = int(old_count)
            bot.user_memory_set(last_not_haha, "haha_count", n + 1)
            logger.debug("added haha for {}".format(last_not_haha))
        else:
            message = "Nice try, {}".format(event.user.full_name)
            yield from bot.coro_send_message(event.conv_id, message)
    else:
        logger.debug("not haha message")
        bot.conversation_memory_set(event.conv_id, "last_not_haha_user_id", event.user_id.chat_id)


def hahas(bot, event, *args):
    """Get the number of your hahas"""
    haha_count = bot.user_memory_get(event.user_id.chat_id, "haha_count")
    message = "{}: {} hahas".format(event.user.full_name, haha_count)
    logger.debug(message)
    yield from bot.coro_send_message(event.conv_id, message)


def scoreboard(bot, event, *args):
    """Get the number of hahas for all users in this hangout"""
    haha_list = {}
    user_list = bot.get_users_in_conversation(event.conv_id)
    for user in user_list:
        splitName = user.full_name.split(" ")
        name = splitName[0]
        if len(splitName) > 1:
            lastname = splitName[1]
            name += " {}.".format(lastname[:1])
        haha_count = bot.user_memory_get(user.id_.chat_id, "haha_count")
        if haha_count is None:
            haha_count = 0
        haha_list[name] = int(haha_count)
    lst = list()
    for key, val in haha_list.items():
        lst.append( (val, key) )
    lst.sort(reverse=True)
    message = "<b>haha scoreboard:</b><br />"
    for (count, name) in lst: 
        message += "{} {}<br />".format(count, name)
    yield from bot.coro_send_message(event.conv_id, message)
