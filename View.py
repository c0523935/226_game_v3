from Board import Board


def display(board: Board) -> None:
    """
    Prints out a Board to stdout.

    :param board: The Board to be displayed on stdout
    """
    print(board)


def display_scores(board: Board) -> None:
    """
    Prints out the scores of all Players.

    :param board: The Board containing the Players
    """
    print(board.get_scores())
