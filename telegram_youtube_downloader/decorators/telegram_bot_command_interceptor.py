from errors.authorization_error import AuthorizationError
from statics.authorization_mode import AuthorizationMode
from utils.config_utils import ConfigUtils
from typing import Awaitable, Callable
from telegram.ext import ContextTypes
from telegram import Update


class TelegramBotCommandInterceptor:
    @staticmethod
    def __is_intersects(user_claims: set, function_claims: set) -> bool:
        return len(user_claims & function_claims) != 0

    @staticmethod
    def secured_command(function_claims: set):
        """Intercepts telegram bot requests and checks for proper authorization"""
        def decorator(func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]):
            async def wrapper(*args, **kwargs):
                authorization_options = ConfigUtils.get_app_config().telegram_bot_options.authorization_options
                selected_authorization_mode = authorization_options.mode

                # Block everyone and allow users on the config with the right claims for this function
                if selected_authorization_mode == AuthorizationMode.ALLOW_SELECTED:
                    users_from_config = authorization_options.users
                    update: Update = args[0];

                    currentUserId = None
                    if update.message and update.message.from_user:
                        currentUserId = update.message.from_user.id
                    else:
                        raise AuthorizationError("Cannot get user id")

                    for user in users_from_config:
                        # Find current user from users on the config file
                        if user.id == currentUserId:
                            # Allow if user has a claim for this function (set intersection)
                            user_claims = set(user.split_claims())
                            if TelegramBotCommandInterceptor.__is_intersects(user_claims, function_claims):
                                return await func(*args, **kwargs)
                            # Block else
                            break

                    # Block if user is not on the allowed list
                    raise AuthorizationError("User is not authorized for this operation")

                # Allow everyone and block users on the config with the right claims for this function
                if selected_authorization_mode == AuthorizationMode.BLOCK_SELECTED:
                    users_from_config = authorization_options.users
                    update: Update = args[0];

                    currentUserId = None
                    if update.message and update.message.from_user:
                        currentUserId = update.message.from_user.id
                    else:
                        raise AuthorizationError("Cannot get user id")

                    for user in users_from_config:
                        # Find current user from users on the config file
                        if user.id == currentUserId:
                            # Block if user has a claim for this function (set intersection)
                            user_claims = set(user.split_claims())
                            if TelegramBotCommandInterceptor.__is_intersects(user_claims, function_claims):
                                raise AuthorizationError("User is not authorized for this operation")
                            # Allow else
                            break

                    # Allow if user is not on the blocked list
                    return await func(*args, **kwargs)

                return await func(*args, **kwargs)
            return wrapper
        return decorator
