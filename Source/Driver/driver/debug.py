from colorama import Fore, Style, Back


def INFO(var: str, text: str, c=Fore.YELLOW, tc=Fore.GREEN):
    print(c + "[INFO]" + Style.RESET_ALL, end=" ")
    print(tc + var + Style.RESET_ALL, end=" ")
    print(c + text + Style.RESET_ALL, end="\n")


def ERROR(var: str, c=Fore.RED, tc=Fore.LIGHTRED_EX):
    print(c + "[ERROR]" + Style.RESET_ALL, end=" ")
    print(tc + var + Style.RESET_ALL, end="\n")
