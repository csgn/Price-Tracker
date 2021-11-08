import time as t
import conf.scripts.time as time
from colorama import Fore, Back, Style


def info(var, message, fore=Fore.LIGHTWHITE_EX):
    print(
        f"{time.now()} - {fore + '[INFO]' + Style.RESET_ALL} :{'':>1}{fore + var + Style.RESET_ALL + ' ' + message.capitalize()}")


def warning(var, message, fore=Fore.LIGHTYELLOW_EX):
    print(
        f"{time.now()} - {fore + '[WARNING]' + Style.RESET_ALL} :{'':>1}{fore+ var + Style.RESET_ALL + ' ' + message.capitalize()}")


def error(var, message, fore=Fore.LIGHTRED_EX):
    print(
        f"{time.now()} - {fore + '[ERROR]' + Style.RESET_ALL} :{'':>1}{fore+ var + Style.RESET_ALL + ' ' + message.capitalize()}")
