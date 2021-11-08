import time as t
import conf.scripts.time as time
from colorama import Fore, Back, Style


def info(var, message):
    print(
        f"{time.now()} - {Fore.LIGHTBLUE_EX + '[INFO]' + Style.RESET_ALL}{'':>1}:\t{Fore.LIGHTWHITE_EX + var + Style.RESET_ALL + ' ' + message.capitalize()}")


def warning(var, message):
    print(
        f"{time.now()} - {Fore.LIGHTYELLOW_EX + '[WARNING]' + Style.RESET_ALL} :\t{Fore.LIGHTWHITE_EX + var + Style.RESET_ALL + ' ' + message.capitalize()}")


def error(var, message):
    print(
        f"{time.now()} - {Fore.LIGHTRED_EX + '[ERROR]' + Style.RESET_ALL} :\t{Fore.LIGHTWHITE_EX + var + Style.RESET_ALL + ' ' + message.capitalize()}")
