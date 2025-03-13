from typing import List, Optional
from enum import Enum
import os

from dacite.config import Config as DaciteConfig
import dacite
import yaml

from data.app_config import AppConfig


class ConfigUtils:
    __nested_env_key_separator = "__" # Should not be used in config file keys
    __config_path = "telegram_youtube_downloader/configs/config.yaml"
    __app_config: Optional[AppConfig] = None


    @staticmethod
    def __read_cfg_file():
        abs_path = os.path.join(os.getcwd(), ConfigUtils.__config_path)
        with open(abs_path, "r") as file:
            cfg = yaml.safe_load(file)
        return cfg


    @staticmethod
    def __set_value_from_nested_keys_recursive(cfg: dict, keys: List[str], current_key_index: int, value: str):
        """
        Recursively set a value in a nested dictionary using a list of keys.
        All values are set as strings and are converted to the correct type when deserializing the config object.
        This function cannot use logging because it is called before the logger is initialized.
        Errors are silently ignored and printed.
        """

        # Validate keys
        if not keys or current_key_index >= len(keys):
            print(f"Invalid keys: {keys}, current_key_index: {current_key_index}")
            return

        current_key = keys[current_key_index]

        # Check for empty keys
        if not current_key:
            print(f"Empty key at index {current_key_index} in keys: {keys}")
            return


        # Convert key to int if it is a digit, so it can be used as a list index
        # Index                v
        # Keys              a__0__c = 1
        if current_key.isdigit():
            current_key = int(current_key)
            # Check for unreasonable list indices
            if current_key < 0:
                return


        # Base case: Last key always single value
        # Index                   v
        # Keys              a__b__c = 1
        # Dict state        a = { b = { } }
        # Set last key      a = { b = { c = 1 } }
        if current_key_index == len(keys) - 1:
            if isinstance(cfg, dict):
                cfg[current_key] = value
            if isinstance(cfg, list):
                if int(current_key) + 1 > len(cfg):
                    cfg.append(value) # List intentionally not padded here
                else:
                    cfg[current_key] = value
            return

        next_key = keys[current_key_index + 1]
        is_next_key_dict_key = not next_key.isdigit()

        # Option 1: Current config object is dict, next key is a dict key
        # Index                v
        # Keys              a__b__c = 1
        # Dict state        a = { }
        # Add new dict      a = { b = { } }

        # Option 2: Current config object is dict, next key is a list key
        # Index                v
        # Keys              a__b__0__c = 1
        # Dict state        a = { }
        # Add new list      a = { b = [] }
        if isinstance(cfg, dict):
            if current_key not in cfg:
                if is_next_key_dict_key:
                    cfg[current_key] = {}
                else:
                    cfg[current_key] = []

        # Option 1: Current config object is list, next key is dict key
        # Index                   v
        # Keys              a__b__0__c = 1
        # Dict state        a = { b = [] }
        # Add new dict      a = { b = [ { c = { } } ] }

        # Option 2: Current config object is list, next key is a list key (This is very unlikely to be used)
        # Index                   v
        # Keys              a__b__0__0__c = 1
        # Dict state        a = { b = [] }
        # Add new list      a = { b = [ [] ] }
        elif isinstance(cfg, list):
            if int(current_key) + 1 > len(cfg):
                if is_next_key_dict_key:
                    cfg.append({})
                if not is_next_key_dict_key:
                    cfg.append([])


        else:
            print(f"Item at key {current_key} is not a dict or list in cfg:{cfg}, skipping")
            return

        # Recursive call
        ConfigUtils.__set_value_from_nested_keys_recursive(cfg[current_key], keys, current_key_index + 1, value)


    @staticmethod
    def __deserialize_config(cfg_dict: dict) -> AppConfig:
        return dacite.from_dict(
            data_class=AppConfig, 
            data=cfg_dict, 
            config=DaciteConfig(
                type_hooks={int: int}, 
                cast=[Enum]
            )
        )


    @staticmethod
    def init_config():
        # Config file for defaults
        cfg = ConfigUtils.__read_cfg_file()

        # Env values overrides defaults
        for key, value in os.environ.items():
            keys = [key] if ConfigUtils.__nested_env_key_separator not in key else key.split(ConfigUtils.__nested_env_key_separator)
            ConfigUtils.__set_value_from_nested_keys_recursive(cfg, keys, 0, value)

        # Deserialize merged config int class
        ConfigUtils.__app_config = ConfigUtils.__deserialize_config(cfg)


    @staticmethod
    def get_app_config() -> AppConfig:
        if not ConfigUtils.__app_config:
            raise Exception(f"Config not initialized. Call {ConfigUtils.init_config.__name__} first")
        return ConfigUtils.__app_config
