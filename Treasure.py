class Treasure:
    def __init__(self, value: int, description: str = '$'):
        """
        Initializes a Treasure.

        :param value: The monetary value of the Treasure
        :param description: The description of the Treasure
        """
        self.value = value
        self.description = description

    def __str__(self):
        return self.description

    def get_value(self) -> int:
        """
        Returns the value of the Treasure.

        :return: The value of the Treasure
        """
        return self.value
