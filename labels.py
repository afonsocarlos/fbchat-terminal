# -*- coding: utf-8 -*-

"""
    Style Labels for Terminal facebook messenger in python.
"""
try:
    from colorama import Fore, Back, Style
    import colorama

    colorama.init()

    START_TITLE = Fore.WHITE + Back.BLUE + Style.BRIGHT  # this is just a string
    START_LABEL = Fore.WHITE + Style.BRIGHT  # this is just a string
    END_TITLE = Style.RESET_ALL
    END_LABEL = Style.RESET_ALL
except ImportError:  # create empty strings just to avoid AttributeError/NameError
    START_TITLE = ""
    START_LABEL = ""
    END_TITLE = ""
    END_LABEL = ""
