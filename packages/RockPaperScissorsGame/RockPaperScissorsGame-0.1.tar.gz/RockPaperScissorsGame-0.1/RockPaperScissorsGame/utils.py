"""
!/usr/bin/env python3
-*- coding: utf-8 -*-
PROGRAMMER: David Mixer
DATE CREATED: 20 June 2021
REVISED DATE: 20 June 2021
PURPOSE: Provide functions commonly used in multiple programs.
"""

from os import system, name
from time import sleep


def clear_screen(sleep_time=0):
    sleep(sleep_time)
    # Issue clear screen command in terminal
    # https://www.geeksforgeeks.org/clear-screen-python/
    if name == 'nt':
        # Windows
        _ = system('cls')
    else:
        # Mac and linux (os.name is 'posix')
        _ = system('clear')
