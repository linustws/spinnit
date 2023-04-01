import html
import io
import json
import math
import random
import time
import traceback
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters

from Logger import Logger
from SpinnerGifMaker import SpinnerGifMaker

telegram_logger = Logger('telegram.ext._application', 'helpJoyMakeDecisions.log')
main_logger = Logger('main', 'helpJoyMakeDecisions.log')

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
                                   text="Oops, something went wrong! Please try again later.")
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called the /start command")
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hamou~ Use me to help you make decisions :D Type "
                                        "/help to see available "
                                        "commands.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called the /help command")
    caps = "/caps - capitalise whatever you say\n"
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Available commands:\n/start - check if the bot is alive\n/help - see "
                                        "available commands\n/spin - spin the wheel")


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} sent a message")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called an unknown command")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def spin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_logger.log('info', f"User {update.effective_user.id} called the /spin command")
    options = context.args
    if not options:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide some options!")
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hmm...thinking, thinking...")
    SpinnerGifMaker(options)
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation='spinner.gif')


if __name__ == '__main__':
    application = ApplicationBuilder().token(***REMOVED***)

    start_handler = CommandHandler('start', start_command)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo_message)
    help_handler = CommandHandler('help', help_command)
    spin_handler = CommandHandler('spin', spin_command)
    # caps_handler = CommandHandler('caps', caps_command)
    # inline_caps_handler = InlineQueryHandler(caps_inline)
    unknown_handler = MessageHandler(filters.COMMAND, unknown_command)

    application.add_error_handler(error_handler)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(help_handler)
    application.add_handler(spin_handler)
    # application.add_handler(caps_handler)
    # application.add_handler(inline_caps_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
