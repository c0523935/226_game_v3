class Player:
    def __init__(self, name: str):
        """
        Creates a new Player with the given name.

        Player score is set to 0.
        :param name: The name of the Player
        """
        self.name = name
        self.score = 0

    def __str__(self):
        return self.name

    def get_name(self) -> int:
        """
        Returns the name.

        :return: The name
        """
        return self.name

    def get_score(self) -> int:
        """
        Returns the score.

        :return: The score
        """
        return self.score

    def add_score(self, value: int) -> None:
        """
        Adds the given value to the Player's score.

        :param value: The value to add.  Can be negative
        """
        self.score += value
