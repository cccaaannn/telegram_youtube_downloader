from errors.authorization_error import AuthorizationError


class TelegramBotErrorHandler:
    @staticmethod
    def command_handler(logger, *, function_name, function_usage):
        """Logs function and error sends message on error"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    logger.info(f"User: {args[0].message.from_user} | Function: {function_name} | Args: {args[1].args}")
                    func(*args, **kwargs)
                except(AuthorizationError) as ae:
                    logger.warning(f"User (not authorized): {args[0].message.from_user} | Function: {function_name} | Args: {args[1].args}")
                    args[0].message.reply_text(str(ae))
                except(IndexError, ValueError):
                    logger.warning(f"User (incorrect function usage): {args[0].message.from_user} | Function: {function_name} | Args: {args[1].args}")
                    if(function_usage == ""):
                        args[0].message.reply_text("Functions did not used properly")
                    else:    
                        args[0].message.reply_text(f"Usage {function_usage}")
                    func(*args, **kwargs)
                except:
                    logger.error(f"User: {args[0].message.from_user} | Function: {function_name} | Args: {args[1].args}", exc_info=True)
                    args[0].message.reply_text("Something went wrong")
            return wrapper
        return decorator

    @staticmethod
    def menu_handler(logger):
        """Logs function and error sends message on error"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    logger.info(f"User: {args[0].callback_query.message.from_user} | Function: {func.__name__} | Args: {args[1].args}")
                    func(*args, **kwargs)
                except:
                    logger.error(f"User:{args[0].callback_query.message.from_user} | Function: {func.__name__} | Args: {args[1].args}", exc_info=True)
                    args[0].callback_query.edit_message_text("Something went wrong", reply_markup=None)
            return wrapper
        return decorator
