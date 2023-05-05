import asyncio
import html
import json
import os
import random
import traceback

import telegram
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters

from logger import Logger
from spinner import Spinner
from rate_limiter import RateLimiter

this_dir = os.path.dirname(__file__)
logger_rel_path = '../../spinnit.log'
logger_abs_path = os.path.join(this_dir, logger_rel_path)
telegram_logger = Logger('telegram.ext._application', logger_abs_path)
main_logger = Logger('main', logger_abs_path)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
DEVELOPER_CHAT_ID = int(os.environ['DEVELOPER_CHAT_ID'])
SPECIAL_IDS = [int(i) for i in os.environ['SPECIAL_IDS'].split()]

is_spinner_down = False
special_mode_dict = {special_id: True for special_id in SPECIAL_IDS}


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    main_logger.log('error', "Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="nani?? something went wrong! come back ltr bah")
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called the /start command")
    user_first_name = update.effective_user.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"hallo {user_first_name} :D type /halp to see what i can do")


async def halp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called the /halp command")
    if update.effective_user.id in SPECIAL_IDS:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="\n/start - check if im alive\n/halp - get help\n/spin - see where "
                                            "your fate lies 💫 (enter each option separated by spaces after the command "
                                            "e.g. /spin eat sleep study)\n/special - choose which pics to see (this "
                                            "is a secret command that is not available to others 😘)")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="\n/start - check if im alive\n/halp - get help\n/spin - see where "
                                            "your fate lies 💫 (enter each option separated by spaces after the command "
                                            "e.g. /spin eat sleep study)")


async def send_random_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == telegram.Chat.PRIVATE:
        main_logger.log('info', f"User {update.effective_user.id} sent a message")
        words = ["mhm mhm", "yes yes", "sheesh", "ok can", "alrites", "g", "wow", "sure", "noice", "unds unds", "frfr",
                 "same", "slay", "noted"]
        response = random.choice(words)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called an unknown command")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="huh idk wym")


async def spin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called the /spin command")
    options = context.args
    if not options:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="enter some options separated with "
                                                                              "spaces after /spin (e.g. /spin eat "
                                                                              "sleep study)")
        return
    if update.effective_user.id in SPECIAL_IDS:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="wait i thinking i thinking")
        asyncio.create_task(
            generate_animation(options, update.effective_chat.id, context, special_mode_dict[update.effective_user.id]))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="wait i thinking i thinking")
        asyncio.create_task(generate_animation(options, update.effective_chat.id, context, False))


async def generate_animation(options, chat_id, context, is_special):
    # start = time.time()
    global is_spinner_down
    gif_path = os.path.join(this_dir, f"{chat_id}.gif")
    try:
        Spinner(chat_id, options, is_special)
        await context.bot.send_animation(chat_id=chat_id, animation=gif_path)
        # end = time.time()
        # await context.bot.send_message(chat_id=chat_id, text=f"Time taken: {end - start} seconds")
    except telegram.error.RetryAfter as e:
        wait_seconds = int(str(e).split("in ", 1)[1].split(" seconds", 1)[0])
        main_logger.log('warning', f"Telegram API rate limit exceeded! Retry after {wait_seconds} seconds")
        await context.bot.send_message(chat_id=chat_id, text="oops i cnt think rn, come back ltr bah")
        if not is_spinner_down:  # only notify the developer if the spinner is not already down
            is_spinner_down = True
            await context.bot.send_message(chat_id=DEVELOPER_CHAT_ID,
                                           text=f"Spinner is down. Waiting {wait_seconds} seconds.")
            await asyncio.sleep(wait_seconds)
            is_spinner_down = False
            await context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text="Spinner is back up.")
    except telegram.error.TimedOut:
        main_logger.log('warning', "Timed out, 'generate_animation' task exception was never retrieved")
    except ValueError as e:
        await context.bot.send_message(chat_id=chat_id, text="too many optionsss")

    if os.path.isfile(gif_path):
        os.remove(gif_path)  # delete the file after sending it, only if it exists


async def special_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global special_mode_dict
    main_logger.log('info', f"User {update.effective_user.id} called the /special command")
    user_input = context.args
    if not user_input:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"special mode: {str(special_mode_dict[update.effective_user.id]).lower()}"
                                            f"\nenter /special [true/false] to choose which pics to see")
        return
    if update.effective_user.id in SPECIAL_IDS:
        if user_input[0].lower() == "true":
            main_logger.log('info', f"User {update.effective_user.id} set special mode to true")
            special_mode_dict[update.effective_user.id] = True
            await context.bot.send_message(chat_id=update.effective_chat.id, text="special mode set to true ❤️")
        elif user_input[0].lower() == "false":
            main_logger.log('info', f"User {update.effective_user.id} set special mode to false")
            special_mode_dict[update.effective_user.id] = False
            await context.bot.send_message(chat_id=update.effective_chat.id, text="special mode set to false 🐱")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="enter /special [true/false] to "
                                                                                  f"choose which pics to see")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="😳 this is a secret command, "
                                                                              "how did u find it :o")


if __name__ == '__main__':
    application = ApplicationBuilder().token(***REMOVED***).read_timeout(
        30).write_timeout(30).build()

    start_handler = CommandHandler('start', start_command)
    random_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), send_random_message)
    halp_handler = CommandHandler('halp', halp_command)
    spin_handler = CommandHandler('spin', spin_command)
    special_handler = CommandHandler('special', special_command)
    unknown_handler = MessageHandler(filters.COMMAND, unknown_command)

    application.add_error_handler(error_handler)
    application.add_handler(start_handler)
    application.add_handler(random_message_handler)
    application.add_handler(halp_handler)
    application.add_handler(spin_handler)
    application.add_handler(special_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
