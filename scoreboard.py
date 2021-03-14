#!/usr/bin/env python3

from typing import List, Tuple, Set, Dict, Union, Optional


class Scoreboard:
    def __init__(self, players: List[str]):
        # len(board[x]) is the width
        # len(board) is the height
        self.board: List[List[Optional[float]]] = [[None for _ in players] for _ in players]
        # A cell needs to fit at least 3 characters because of decimal numbers.
        # We will not have numbers larger than 10 because of the cap on 8
        # players.
        self.cell_width = max(3, max(map(len, players)))
        self.players = players
        list.sort(self.players, key=str.lower)

    def add_score(self, a: int, b: int, score: float):
        cell = self.board[a][b]
        if cell is None:
            self.board[a][b] = score
            self.board[b][a] = 0
        elif cell is not None:
            self.board[a][b] = cell + score

    def get_pair_result(self, player: str, against: str) -> str:
        player_score = sum_maybe(self.board[self.players.index(player)])
        against_score = sum_maybe(self.board[self.players.index(against)])
        if player_score <= against_score + 0.1 and player_score >= against_score - 0.1:
            return "draw"
        elif player_score > against_score:
            return "winner"
        else:
            return "loser"

    def add_draw(self, a: str, b: str):
        self.add_score_by_name(a, b, 0.5)
        self.add_score_by_name(b, a, 0.5)

    def add_winner(self, winner: str, loser: str):
        self.add_score_by_name(winner, loser, 1)

    def add_score_by_name(self, a: str, b: str, score: float):
        self.add_score(self.players.index(a),
                       self.players.index(b),
                       score)

    def display(self):
        print('\n-----Scoreboard-----')
        print(self.to_string())

    def to_string(self):
        """Transform into a string representation.

        Note that it performs the computation each time it's called. If repeated
        calls are needed rewrite this to cache the string representation in the object.
        """
        strboard = [" " * self.cell_width +
                    "| " +
                    " ".join(map(lambda x: x.center(self.cell_width), self.players))]
        strboard.append(["_"] * len(strboard[0]))
        strboard[1][self.cell_width] = "|"
        strboard[1] = "".join(strboard[1])
        for p in range(0, len(self.players)):
            tmp = [(self.players[p].ljust(self.cell_width) + "|")]
            for i in range(0, len(self.board[p])):
                cell = str(self.board[p][i])
                if self.board[p][i] is None:
                    cell = ' '

                tmp.append('X' if i == p else cell)
            strboard.append(" ".join(map(lambda x: x.center(self.cell_width), tmp)))

        return "\n".join(strboard)

    def get_results(self):
        cell_width = max(len("Player"), self.cell_width)
        rows = ["| " + "Player".center(cell_width) + " | " + "Result".ljust(6) + " |"]
        for p in range(0, len(self.players)):
            name = self.players[p].ljust(cell_width)
            result = str(sum_maybe(self.board[p])).rjust(6)  # 3 = len("Result")
            rows.append("| " + name + " | " + result + " |")
        return "\n".join(rows)

    def display_results(self):
        print('\n-----Results-----')
        print(self.get_results())


def sum_maybe(xs: List[Optional[float]]) -> float:
    """
    Compute the sum of xs ignoring all Nones
    """
    s: float = 0
    for x in xs:
        if x is not None:
            s = s + x
    return s
