from errors.authorization_error import AuthorizationError
from typing import Awaitable, Callable
from telegram.ext import ContextTypes
from telegram import Update
from logging import Logger


class TelegramBotErrorHandler:
    @staticmethod
    def command_handler(logger: Logger, command_usage: str):
        """Logs function and error sends message on error"""
        def decorator(func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]):
            async def wrapper(*args, **kwargs):
                update: Update = args[0];
                context: ContextTypes.DEFAULT_TYPE = args[1];
                try:
                    logger.info(f"Update: {update} | Args: {context.args}")
                    await func(*args, **kwargs)

                # Authorization error
                except(AuthorizationError) as ae:
                    logger.warning(f"Update: {update} | Args: {context.args} | Error: {ae}")
                    await update.message.reply_text(str(ae))

                # Command usage error
                except(IndexError, ValueError) as e:
                    logger.warning(f"Update: {update} | Args: {context.args} | Error: {e}")
                    if(command_usage == ""):
                        await update.message.reply_text("Functions did not used properly")
                    else:    
                        await update.message.reply_text(f"Command usage: {command_usage}")

                # Other errors
                except:
                    logger.error(f"Update: {update} | Args: {context.args}", exc_info=True)
                    await update.message.reply_text("Something went wrong")

            return wrapper
        return decorator

    @staticmethod
    def menu_handler(logger: Logger):
        """Logs function and error sends message on error"""
        def decorator(func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]):
            async def wrapper(*args, **kwargs):
                update: Update = args[0];
                context: ContextTypes.DEFAULT_TYPE = args[1];
                try:
                    logger.info(f"Update: {update} | Args: {context.args}")
                    await func(*args, **kwargs)
                except:
                    logger.error(f"Update: {update} | Args: {context.args}", exc_info=True)
                    await update.callback_query.edit_message_text("Something went wrong", reply_markup=None)
            return wrapper
        return decorator
