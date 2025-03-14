from typing import Awaitable, Callable
import logging

from telegram.ext import ContextTypes
from telegram import Update

from errors.authorization_error import AuthorizationError


class TelegramBotErrorHandler:
    __logger = logging.getLogger(f"tyd.{__name__}")

    @staticmethod
    def command_handler(command_usage: str):
        """Logs function and error sends message on error"""
        def decorator(func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]):
            async def wrapper(*args, **kwargs):
                update: Update = args[0];
                context: ContextTypes.DEFAULT_TYPE = args[1];
                try:
                    TelegramBotErrorHandler.__logger.info(f"Update: {update} | Args: {context.args}")
                    await func(*args, **kwargs)

                # Authorization error
                except(AuthorizationError) as ae:
                    TelegramBotErrorHandler.__logger.warning(f"Update: {update} | Args: {context.args} | Error: {ae}")
                    if not update.message:
                        TelegramBotErrorHandler.__logger.error(f"Cannot reply update: {update} | Args: {context.args}")
                        return

                    await update.message.reply_text(str(ae))

                # Command usage error
                except(IndexError, ValueError) as e:
                    TelegramBotErrorHandler.__logger.warning(f"Update: {update} | Args: {context.args} | Error: {e}")
                    if not update.message:
                        TelegramBotErrorHandler.__logger.error(f"Cannot reply update: {update} | Args: {context.args}")
                        return

                    if(command_usage == ""):
                        await update.message.reply_text("Functions did not used properly")
                    else:    
                        await update.message.reply_text(f"Command usage: {command_usage}")

                # Other errors
                except:
                    TelegramBotErrorHandler.__logger.error(f"Update: {update} | Args: {context.args}", exc_info=True)
                    if not update.message:
                        TelegramBotErrorHandler.__logger.error(f"Cannot reply update: {update} | Args: {context.args}")
                        return
                    await update.message.reply_text("Something went wrong")

            return wrapper
        return decorator

    @staticmethod
    def menu_handler():
        """Logs function and error sends message on error"""
        def decorator(func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]):
            async def wrapper(*args, **kwargs):
                update: Update = args[0];
                context: ContextTypes.DEFAULT_TYPE = args[1];
                try:
                    TelegramBotErrorHandler.__logger.info(f"Update: {update} | Args: {context.args}")
                    await func(*args, **kwargs)
                except:
                    TelegramBotErrorHandler.__logger.error(f"Update: {update} | Args: {context.args}", exc_info=True)
                    if not update.callback_query:
                        TelegramBotErrorHandler.__logger.error(f"Cannot reply update: {update} | Args: {context.args}")
                        return
                    await update.callback_query.edit_message_text("Something went wrong", reply_markup=None)
            return wrapper
        return decorator
