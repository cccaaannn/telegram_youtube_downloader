from telegram_bot import run_bot
import argparse
import os

def __read_from_file(file_name):
    try:
        with open(file_name,'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except (OSError, IOError) as e:
        print(e)

def path(p):
    if(os.path.isfile(p)):
        return p
    else:
        raise argparse.ArgumentTypeError("file does not exists")


bot_key_env_name = "TELEGRAM_BOT_KEY"

parser = argparse.ArgumentParser()

mutually_exclusive_group = parser.add_mutually_exclusive_group(required=True)
mutually_exclusive_group.add_argument("-k", "--use_key", dest="use_key", metavar="<key>", type=str, help="Telegram bot key")
mutually_exclusive_group.add_argument("-e", "--use_env", dest="use_env", action="store_true", help="Use environment variable <{0}> for the Telegram bot key".format(bot_key_env_name))
mutually_exclusive_group.add_argument("-f", "--use_file", dest="use_file", metavar="<path>", type=path, help="File path for Telegram bot key")

args = parser.parse_args()

if(args.use_key):
    run_bot(args.use_key)
elif(args.use_env):
    run_bot(os.environ[bot_key_env_name])
elif(args.use_file):
    key = __read_from_file(args.use_file)
    run_bot(key)
else:
    parser.error("No arguments specified")


