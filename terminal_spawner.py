import sys
import subprocess


def spawn_player_terminal(i):
    # For Linux:
    if sys.platform.startswith('linux'):
        return subprocess.Popen(["xterm", "-e", "python3", "player_terminal.py",  "--id", f"{i}"])
        # os.system(f"gnome-terminal -- python3 player_terminal.py --id {i}")
    elif sys.platform.startswith('win32'):
        return subprocess.Popen(
            [sys.executable, "player_terminal.py", "--id", f"{i}"],
            creationflags=subprocess.CREATE_NEW_CONSOLE)
       # os.system(f'start cmd /k player_terminal.py --id {i}')


def spawn_tournament_manager_terminal(game_type):
    # For Linux:
    if sys.platform.startswith('linux'):
        return subprocess.Popen(["xterm", "-e", "python3", "tournament_manager.py", "--game_type", f"{game_type}"])
        # os.system(f"gnome-terminal -- python3 tournament_manager.py --game_type {game_type}")
    elif sys.platform.startswith('win32'):
        return subprocess.Popen(
            [sys.executable, "tournament_manager.py", "--game_type", f"{game_type}"],
            creationflags=subprocess.CREATE_NEW_CONSOLE)
        # os.system(f'start cmd /k tournament_manager.py --game_type {game_type}')


def player_terminal_spawner(n, players):
    # Spawn 2 Player Terminals
    mjobs = []
    # if sys.platform.startswith('linux'):

    for i in range(n):
        p = spawn_player_terminal(players[i])
        mjobs.append(p)
    return mjobs

    # elif sys.platform.startswith('win32'):
    #     for i in range(n):
    #         p = mp.Process(target=spawn_player_terminal, args=(players[i],))
    #         mjobs.append(p)
    #         p.start()
    #     for j in mjobs:
    #         j.join()
    #     return mjobs


def tournament_manager_terminal_spawner(game_type):
    spawn_tournament_manager_terminal(game_type).wait()

    # if sys.platform.startswith('linux'):
    #     spawn_tournament_manager_terminal(game_type).wait()
    # elif sys.platform.startswith('win32'):
    #     p = mp.Process(target=spawn_tournament_manager_terminal, args=(game_type,))
    #     p.start()
    #     p.join()

# if __name__ == '__main__':
#     terminal_spawner(2)
