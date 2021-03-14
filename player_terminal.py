import argparse
import os
import re


def write_to_file(filename, pname, user_input):
    file1 = open(filename, 'a')
    file1.write(pname+'-'+user_input+'\n')
    file1.close()


def write_pid(filename, processid):
    file1 = open(filename, 'a')
    file1.write(str(processid)+'\n')
    file1.close()


def main_loop(pname):

    write_pid('player-processid.txt', os.getpid())
    # print(os.getpid())

    filename = 'PvP.txt'
    print(f"Welcome Player {pname}")
    while True:
        user_input = input("> ")
        if user_input == "q" or user_input == "s":
            write_to_file(filename, pname, user_input)
        else:
            if re.match("^[0-9]-[0-9]$", user_input): # chang erule here
                write_to_file(filename, pname, user_input)
                # print('Move Successful')
            else:
                print('Invalid input')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Player Terminal")
    parser.add_argument('-i', '--id', type=str, help='Terminal ID', required=True)
    args = parser.parse_args()
    main_loop(args.id)
