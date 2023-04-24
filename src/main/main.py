import asyncio
import html
import json
import os
import time
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
from unposterised_no_mp_optimised import SpinnerGifMaker

telegram_logger = Logger('telegram.ext._application', 'help_joy_decide.log')
main_logger = Logger('main', 'help_joy_decide.log')

DEVELOPER_CHAT_ID = ***REMOVED***


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
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="hamou~ enter /help to see available commands")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called the /help command")
    caps = "/caps - capitalise whatever you say\n"
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="\n/start - check if the bot is alive\n/help - see "
                                        "available commands\n/decide - help you decide")


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} sent a message")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called an unknown command")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="huh idk wym")


async def spin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called the /decide command")
    options = context.args
    allowed_ids = [***REMOVED***, ***REMOVED***]
    if update.effective_user.id not in allowed_ids:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ps this bot is made only for joy "
                                                                              "rn 🙃 i'll release one that can be "
                                                                              "customised soon~")
    else:
        if not options:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="enter some options separated with "
                                                                                  "spaces after /decide")
            return
        await context.bot.send_message(chat_id=update.effective_chat.id, text="wait i thinking i thinking")
        asyncio.create_task(generate_animation(options, update.effective_chat.id, context))


async def generate_animation(options, chat_id, context):
    start = time.time()
    try:
        SpinnerGifMaker(options)
        await context.bot.send_animation(chat_id=chat_id, animation='src/main/spinner.gif')
        os.remove('src/main/spinner.gif')  # delete the file after sending it
        end = time.time()
        # await context.bot.send_message(chat_id=chat_id, text=f"Time taken: {end - start} seconds")
    except telegram.error.RetryAfter as e:
        main_logger.log('warning', "Telegram API rate limit exceeded!")
        await context.bot.send_message(chat_id=chat_id, text="ps i cnt think rn, come back ltr bah")
    except ValueError as e:
        await context.bot.send_message(chat_id=chat_id, text="too many optionsss")


if __name__ == '__main__':
    application = ApplicationBuilder().token(***REMOVED***).read_timeout(
        30).write_timeout(30).build()

    start_handler = CommandHandler('start', start_command)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo_message)
    help_handler = CommandHandler('help', help_command)
    spin_handler = CommandHandler('decide', spin_command)
    unknown_handler = MessageHandler(filters.COMMAND, unknown_command)

    application.add_error_handler(error_handler)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(help_handler)
    application.add_handler(spin_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
