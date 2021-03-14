import argparse
import random
import subprocess
import sys
from itertools import combinations

from scoreboard import Scoreboard
from terminal_spawner import player_terminal_spawner


def display_gameboard(gameboard):
    print()
    print('############################################################################')
    for row in gameboard:
        for col in row:
            print(col, end=' ')
        print()


def generate_game_board():
    gameboard = [['-' for i in range(9)] for j in range(9)]
    return gameboard


def update_gameboard(gameboard, players, player_name, player_move):
    # Player 0 - X, Player 1 - O
    print(player_name, player_move)
    if player_name == players[0]:
        gameboard[player_move[0]][player_move[1]] = 'X'
    else:
        gameboard[player_move[0]][player_move[1]] = 'O'
    return gameboard


def is_game_over(gameboard):
    if gameboard[0][0] != '-':
        return True
    else:
        return False


def read_match_file():
    with open("PvP.txt", "r") as f:
        lines = f.readlines()
    return lines


def terminate_player_terminals(mjobs):
    if sys.platform.startswith('linux'):
        for job in mjobs:
            job.terminate()

    elif sys.platform.startswith('win32'):
        with open("player-processid.txt", "r") as f:
            lines = f.readlines()
        for i in lines:
            subprocess.Popen("TASKKILL /F /PID {pid} /T".format(
                pid=int(i.rstrip())))


def generate_tournament_schedule(players):
    # input -> List[str]
    # output -> List[Tuple[str,str]]
    # Example:
    # generate_tournament_schedule(['A','B','C','D']) -> [('B', 'D'),
    #  ('A', 'C'), ('A', 'D'), ('A', 'B'), ('C', 'D'), ('B', 'C')]]

    games_to_play = list(combinations(players, 2))
    shuffled_game = []
    for game in games_to_play:
        shuffled_game.append(tuple(random.sample(game, len(game))))
    random.shuffle(shuffled_game)
    return shuffled_game


def input_player_info(num_players):
    print('Enter Player Names:-')
    players = []
    while len(players) != num_players:
        pname = input('Player Name: ')
        if pname == 'q':
            exit(1)
        if '-' in pname:
            print('Hyphens are not allowed in the name')
        elif len(pname) > 20 or len(pname) <= 0:
            print('Name length should be between 1 and 20')
        elif pname in players:
            print('Duplicate names not allowed')
        else:
            players.append(pname)
    return players


def save_schedule(players):
    """
    Save the players and a round robin schedule to schedule.txt
    """
    schedule = generate_tournament_schedule(players)

    open('schedule.txt', 'w').close()

    with open('schedule.txt', 'a') as f:
        f.write("-".join(players) + '\n')
        for match in schedule:
            f.write(match[0]+'-'+match[1]+'\n')

    return schedule


def display_schedule(schedule):
    print('\nSCHEDULE:')
    for i in range(len(schedule)):
        print('MATCH '+str(i+1)+')', schedule[i][0]+' VS ' + schedule[i][1])
    print()


def manage_tournament(game_type):
    print('I am the Tournament Manager!\n')
    if game_type == 'single':
        players = ['Player1', 'Player2']
        save_schedule(players)
    else:
        succeeds = False
        while not succeeds:
            succeeds = True
            try:
                num_players = input('Number of Players: ')
                if num_players == 'q':
                    exit(1)
                if not num_players.isnumeric():
                    print('Non-numeric input is not allowed')
                    succeeds = False
                else:
                    num_players = int(num_players)
                    if num_players > 8 or num_players < 3:
                        print('Number of players should be between 3 and 8')
                        succeeds = False

            except ValueError:
                succeeds = False
        players = input_player_info(num_players)
        display_schedule(save_schedule(players))

    with open("schedule.txt", "r") as schedule:
        schedule = schedule.readlines()
        player_names = schedule[0].rstrip().split('-')
        quitted_players = []
        scoreboard = Scoreboard(player_names)
        for match in schedule[1:]:
            # Clear PvP.txt and player-processid.txt
            open('PvP.txt', 'w').close()
            open('player-processid.txt', 'w').close()
            surrendered = False

            players = match.rstrip().split('-')
            if players[0] in quitted_players and players[1] in quitted_players:
                continue
            if players[0] in quitted_players:
                scoreboard.add_score_by_name(players[1], players[0], 1)
                continue

            if players[1] in quitted_players:
                scoreboard.add_score_by_name(players[0], players[1], 1)
                continue

            print(players[0] + ' VS ' + players[1])
            mjobs = player_terminal_spawner(2, players)

            gameboard = generate_game_board()
            display_gameboard(gameboard)

            # Keep reading PvP.txt for player moves until game is over
            previous_match_file = read_match_file()

            # Determines which player's turn it is
            current_player = 0
            print(players[current_player]+"'s turn")
            surrending_player = -1
            winning_player = -1

            while not is_game_over(gameboard) and not surrendered:
                for i in range(0, len(players)):
                    mjobs[i].poll()
                    # Check if process has terminated
                    if mjobs[i].returncode is not None:
                        quitted_players.append(players[i])
                        print(players[i] + "has quit the tournament!")
                        surrending_player = i
                        winning_player = (surrending_player + 1) % 2
                        surrendered = True
                current_match_file = read_match_file()
                # Do something only if one of the players has made an input
                if previous_match_file != current_match_file:
                    for line in current_match_file:
                        if line not in previous_match_file:
                            line = line.rstrip().split('-')

                            if line[1] == 's':
                                surrendered = True
                                surrending_player = players.index(line[0])
                                winning_player = (surrending_player + 1) % 2
                            elif line[1] == 'q':
                                surrendered = True
                                surrending_player = players.index(line[0])
                                winning_player = (surrending_player + 1) % 2
                                quitted_players.append(players[0])
                            else:
                                # Check if current player has played
                                if line[0] == players[current_player]:
                                    gameboard = update_gameboard(
                                        gameboard, players, player_name=line[0],
                                        player_move=(int(line[1]),
                                                     int(line[2])))
                                    display_gameboard(gameboard)

                                    # Switch current player
                                    current_player = 0 if current_player == 1 else 1
                                    print(players[current_player]+"'s Turn:")

                                else:
                                    print("It is not %s's turn!" % line[0])

                    previous_match_file = current_match_file
            if surrendered:
                scoreboard.add_score_by_name(players[winning_player], players[surrending_player], 1)
            else:
                # TODO properly implement who lost and assign score
                scoreboard.add_score_by_name(players[0], players[1], 1)

            terminate_player_terminals(mjobs)

            print('===============================================================================================')
            print('GAME OVER')
            print('===============================================================================================')
            print()
        # Give players a chance to see the scoreboard

        if game_type == 'single':
            res = scoreboard.get_pair_result(players[0], players[1])
            if res == "draw":
                print("The result is a draw!")
            elif res == "winner":
                print(f"{players[0]} is the winner!")
            else:
                print(f"{players[1]} is the winner!")
        else:
            scoreboard.display()
            scoreboard.display_results()

        input("\nContinue?")
        # TODO: Close all terminals


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tournament Manager Terminal")
    parser.add_argument('-game_type', '--game_type', type=str, help='Game Type', required=True)
    args = parser.parse_args()
    manage_tournament(args.game_type)
