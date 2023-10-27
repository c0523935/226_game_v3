from Treasure import Treasure
from Player import Player


class Tile:
    def __init__(self, treasure: Treasure = None, description: str = '.'):
        """
        Initializes a Tile.

        :param treasure: A Treasure associated with the current Tile, if any
        :param description: A description of the Tile
        """
        self.treasure = treasure
        self.description = description
        self.player = None

    def __str__(self):
        player_str = ' ' if self.player is None else str(self.player)
        treasure_str = ' ' if self.treasure is None else str(self.treasure)
        return f' {treasure_str}{self.description}{player_str} '

    def get_treasure(self) -> any:
        """
        Returns the Treasure associated with this Tile, if any.

        :return: The Treasure, or None if there is none
        """
        return self.treasure

    def set_treasure(self, treasure: Treasure) -> None:
        """
        Adds a Treasure to the Tile.

        :param treasure: The Treasure to be added.  Raises a ValueError if there already is a Treasure
        """
        if self.treasure is not None:
            raise ValueError("Treasure already exists")

        self.treasure = treasure

    def add_player(self, player: Player) -> int:
        """
        Adds a Player to the Tile.

        If there is a Treasure associated with the Tile, it is removed and its value added to the Player's score
        :param player: The Player to be added.  Raises a ValueError if there already is a Player on this Tile
        :return: If there is a Treasure, the value of the Treasure, else 0
        """
        if self.player is not None:
            raise ValueError("Tile already occupied")

        self.player = player
        if self.treasure is not None:
            val = self.treasure.get_value()
            self.player.add_score(val)
            self.treasure = None
            return val

        return 0

    def remove_player(self) -> None:
        """
        Removes a Player from the Tile, if possible.
        """
        self.player = None
