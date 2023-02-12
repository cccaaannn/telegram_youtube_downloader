from errors.authorization_error import AuthorizationError
from statics.authorization_mode import AuthorizationMode
from utils.config_utils import ConfigUtils


class TelegramBotCommandInterceptor:
    @staticmethod
    def is_intersects(user_claims: set, function_claims: set) -> bool:
        return len(user_claims & function_claims) != 0

    @staticmethod
    def secured_command(function_claims: set):
        """Intercepts telegram bot requests and checks for proper authorization"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                authorization_options = ConfigUtils.read_cfg_file()["telegram_bot_options"]["authorization_options"]
                selected_authorization_mode = authorization_options.get("mode", AuthorizationMode.DISABLED.value)

                # Block everyone and allow users on the config with the right claims for this function
                if selected_authorization_mode == AuthorizationMode.ALLOW_SELECTED.value:
                    users_from_config = authorization_options.get("users", [])
                    currentUserId = args[0].message.from_user.id

                    for user in users_from_config:
                        # Find current user from users on the config file
                        if user["id"] == currentUserId:
                            # Allow if user has a claim for this function (set intersection)
                            user_claims = set(user["claims"].split(","))
                            if TelegramBotCommandInterceptor.is_intersects(user_claims, function_claims):
                                return func(*args, **kwargs)
                            # Block else
                            break

                    # Block if user is not on the allowed list
                    raise AuthorizationError("User is not authorized for this operation")

                # Allow everyone and block users on the config with the right claims for this function
                if selected_authorization_mode == AuthorizationMode.BLOCK_SELECTED.value:
                    users_from_config = authorization_options.get("users", [])
                    currentUserId = args[0].message.from_user.id

                    for user in users_from_config:
                        # Find current user from users on the config file
                        if user["id"] == currentUserId:
                            # Block if user has a claim for this function (set intersection)
                            user_claims = set(user["claims"].split(","))
                            if TelegramBotCommandInterceptor.is_intersects(user_claims, function_claims):
                                raise AuthorizationError("User is not authorized for this operation")
                            # Allow else
                            break

                    # Allow if user is not on the blocked list
                    return func(*args, **kwargs)

                return func(*args, **kwargs)
            return wrapper
        return decorator
