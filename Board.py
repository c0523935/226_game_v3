from random import randrange
from Tile import Tile
from Treasure import Treasure
from Player import Player
from enum import Enum


class Direction(Enum):
    UP = 'UP'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    DOWN = 'DOWN'


class Board:
    def __init__(self, n: int, t: int, min_val: int, max_val: int, max_players: int):
        """
        Initializes a Board.

        Treasures are given random values and are randomly placed on this Board.
        :param n: The dimension of the 2D Board; raises a ValueError if n < 2
        :param t: The number of treasures in the Board; raises a ValueError if n < t or t < 0
        :param min_val: The minimum value of a Treasure; raises a ValueError if min_val < 1
        :param max_val: The maximum value of a Treasure; raises a ValueError if max_val < min_val
        :param max_players: The maximum number of Players; raises a ValueError if max_players < 0 or n < max_players
        """
        if n < 2:
            raise ValueError("n must not be less than 2")

        if t < 0:
            raise ValueError("n must not be less than 0")

        if n < t:
            raise ValueError("n must not be less than t")

        if min_val < 1:
            raise ValueError("min_val must not be less than 1")

        if max_val < min_val:
            raise ValueError("max_val must not be less than min_val")

        if max_players < 0 or n < max_players:
            raise ValueError("max_players must be in range 0 <= max_players <= n")

        self.game_board = [[Tile() for _ in range(n)] for _ in range(n)]

        self.num_treasures = t
        for _ in range(self.num_treasures):
            while True:
                x = randrange(n)
                y = randrange(n)
                if self.game_board[x][y].get_treasure() is None:
                    self.game_board[x][y].set_treasure(Treasure(randrange(min_val, max_val + 1)))
                    break

        self.max_players = max_players
        self.players = {}

    def __str__(self):
        board_string = ''
        for row in self.game_board:
            for cell in row:
                board_string += str(cell)
            board_string += '\n'

        return board_string

    def get_scores(self) -> str:
        """
        Returns a listing of all players and their scores.

        :return: A listing of all players and their scores
        """
        score_string = ''
        for (p, (_, _)) in self.players.values():
            score_string += f'{p.get_name()}: {p.get_score()}\n'

        return score_string

    def get_score_list(self) -> [int]:
        """
        Returns a list of all players scores, sorted by player name in ascending order.

        :return: A list of all player scores
        """
        score_list = []
        sorted_keys = sorted(self.players.keys())
        for k in sorted_keys:
            p, (_, _) = self.players[k]
            score_list += [p.get_score()]

        return score_list

    def add_player(self, name: str, x: int, y: int) -> None:
        """
        Add a Player with the given name to the Tile at the given Board position.

        If there is a Treasure at the given location, it is removed and its value added to the Player's score.
        :param name: The name of the Player to be added; raises a ValueError if the name already exists or there are too
         many Players
        :param x: The x position of the Player; raises a ValueError if x is not in range 0 <= x < n or a Player already
         is at that location, n being the row size
        :param y: The y position of the Player; raises a ValueError if y is not in range 0 <= y < n or a Player already
         is at that location, n being the column size
        """
        n = len(self.game_board)
        if not (0 <= x < n):
            raise ValueError("x is not in range 0 <= x < n")

        if not (0 <= y < n):
            raise ValueError("y is not in range 0 <= y < n")

        if name in self.players:
            raise ValueError("name already exists")

        if len(self.players) == self.max_players:
            raise ValueError("cannot add any more players")

        p = Player(name)
        if self.game_board[x][y].add_player(p) > 0:
            self.num_treasures -= 1
        self.players[name] = (p, (x, y))

    def move_player(self, name: str, direction: Direction) -> int:
        """
        Move the Player with the given name in the given Direction.

        Any Treasure at the new location is picked up by the Player, and the score is updated accordingly.
        :param name: The name of the Player to be moved.  Raises a ValueError if the Player does not exist
        :param direction: The Direction in which the Player should move.  Raises a ValueError if that is not possible.
        :return: The value of the picked-up Treasure, or 0 if there was no Treasure
        """
        if name not in self.players:
            raise ValueError("no such player exists")

        (p, (x, y)) = self.players[name]
        new_x = x
        new_y = y
        match direction:
            case Direction.UP:
                if x == 0:
                    raise ValueError("already at the top")
                new_x = x - 1
            case Direction.LEFT:
                if y == 0:
                    raise ValueError("already at the left edge")
                new_y = y - 1
            case Direction.RIGHT:
                if y == len(self.game_board) - 1:
                    raise ValueError("already at the right edge")
                new_y = y + 1
            case Direction.DOWN:
                if x == len(self.game_board) - 1:
                    raise ValueError("already at the bottom")
                new_x = x + 1
            case _:
                raise ValueError("unexpected direction")

        if self.game_board[new_x][new_y].player is not None:
            raise ValueError("already occupied")

        self.players[name] = (p, (new_x, new_y))
        self.game_board[x][y].remove_player()
        value = self.game_board[new_x][new_y].add_player(p)
        if value > 0:
            self.num_treasures -= 1

        return value

    def game_over(self) -> bool:
        """
        Returns whether the game is over.

        The game is over when there are no more Treasures to be found.
        :return: True if the game is over, False otherwise
        """
        return self.num_treasures == 0
