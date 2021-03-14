#!/usr/bin/env python3
from itertools import combinations
from typing import Callable, Dict, List, Set, Tuple

from terminal_spawner import tournament_manager_terminal_spawner


def main():
    choice_map = {'g': start_game,
                  'a': start_game_against_ai,
                  't': start_tournament,
                  'q': quit}
    while (True):
        display_menu(choice_map,
                     """Welcome to the main menu.
                     [g] start a game
                     [a] start a game against an AI
                     [t] Start a tournament
                     [q]uit
                     """)


def display_menu(choice_map: Dict[str, Callable[[], None]], text):
    print(text)
    fun = None
    user_input = ""
    while fun is None:
        user_input = input("> ")
        if user_input in choice_map:
            fun = choice_map.get(user_input[0])
        else:
            print('Invalid option chosen')
    fun()


def start_game_against_ai():
    print("Start game against AI!")
    print('-- PENDING --')


def start_game():
    print("Start game!")
    tournament_manager_terminal_spawner('single')


def start_tournament():
    print('Tournament')
    tournament_manager_terminal_spawner('tournament')


def quit():
    print("Bye!")
    exit(0)


if __name__ == "__main__":
    main()
