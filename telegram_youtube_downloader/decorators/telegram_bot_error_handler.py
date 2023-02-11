class TelegramBotErrorHandler:
    @staticmethod
    def command_handler(logger, function_usage=""):
        """Logs function and error sends message on error"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    logger.info(f"Function: {func.__name__} User: {args[0].message.from_user} Args: {args[1].args}")
                    func(*args, **kwargs)
                except(IndexError, ValueError):
                    logger.warning(f"function: {func.__name__} User: {args[0].message.from_user} Args: {args[1].args}")
                    if(function_usage == ""):
                        args[0].message.reply_text("Functions did not used properly")
                    else:    
                        args[0].message.reply_text(f"Usage {function_usage}")
                except:
                    logger.error(f"function: {func.__name__} User:{args[0].message.from_user} Args: {args[1].args}", exc_info=True)
                    args[0].message.reply_text("Something went wrong")
            return wrapper
        return decorator

    @staticmethod
    def menu_handler(logger):
        """Logs function and error sends message on error"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    logger.info(f"Function: {func.__name__} User: {args[0].callback_query.message.from_user} Args: {args[1].args}")
                    func(*args, **kwargs)
                except:
                    logger.error(f"function: {func.__name__} User:{args[0].callback_query.message.from_user} Args: {args[1].args}", exc_info=True)
                    args[0].callback_query.edit_message_text("Something went wrong", reply_markup=None)
            return wrapper
        return decorator
