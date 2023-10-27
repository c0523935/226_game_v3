import pytest

from Board import Board, Direction
from Player import Player
from Tile import Tile
from Treasure import Treasure


def test_treasure():
    t1 = Treasure(10)
    t2 = Treasure(20, description='%')

    assert t1.value == t1.get_value() == 10
    assert t1.description == str(t1) == '$'
    assert t2.value == t2.get_value() == 20
    assert t2.description == str(t2) == '%'


def test_player():
    p = Player('michael')

    assert p.name == str(p) == 'michael'
    assert p.score == p.get_score() == 0

    p.add_score(10)
    assert p.score == p.get_score() == 10


def test_tile():
    t1 = Treasure(10)
    t2 = Treasure(20)
    p1 = Player('1')
    p2 = Player('2')

    tile1 = Tile()
    tile2 = Tile(t2, '#')

    assert tile1.treasure == tile1.get_treasure()
    assert tile1.treasure is None
    assert tile1.description == '.'
    assert tile1.player is None
    assert str(tile1) == '  .  '

    assert tile2.treasure == tile2.get_treasure() == t2
    assert tile2.description == '#'
    assert tile2.player is None
    assert str(tile2) == ' $#  '

    tile1.set_treasure(t1)
    with pytest.raises(ValueError, match='Treasure already exists'):
        tile1.set_treasure(t2)
    assert tile1.treasure == tile1.get_treasure() == t1

    assert tile2.add_player(p2) == 20
    assert str(tile2) == '  #2 '
    with pytest.raises(ValueError, match='Tile already occupied'):
        tile2.add_player(p1)
    assert tile2.player == p2
    assert tile2.player.score == p2.get_score() == 20

    tile2.remove_player()
    assert tile2.player is None
    assert tile2.add_player(p1) == 0
    assert str(tile2) == '  #1 '
    assert tile2.player == p1
    assert tile2.player.score == p1.get_score() == 0


def test_board():
    with pytest.raises(ValueError, match='n must not be less than 2'):
        _ = Board(1, 5, 5, 10, 2)

    with pytest.raises(ValueError, match='n must not be less than t'):
        _ = Board(2, 5, 5, 10, 2)

    with pytest.raises(ValueError, match='n must not be less than 0'):
        _ = Board(2, -5, 5, 10, 2)

    with pytest.raises(ValueError, match='min_val must not be less than 1'):
        _ = Board(10, 5, 0, 10, 2)

    with pytest.raises(ValueError, match='max_val must not be less than min_val'):
        _ = Board(10, 5, 5, 4, 2)

    with pytest.raises(ValueError, match='max_players must be in range 0 <= max_players <= n'):
        _ = Board(10, 5, 5, 10, -1)

    b = Board(10, 5, 5, 5, 0)
    assert len(b.game_board) == 10
    assert b.num_treasures == 5
    assert b.max_players == 0
    assert len(b.players) == 0

    with pytest.raises(ValueError, match='max_players must be in range 0 <= max_players <= n'):
        _ = Board(10, 5, 5, 10, 11)

    b = Board(10, 5, 5, 10, 10)
    assert len(b.game_board) == 10
    assert b.num_treasures == 5
    assert b.max_players == 10
    assert len(b.players) == 0

    num_t = 0
    for row in b.game_board:
        assert len(row) == 10
        for cell in row:
            if cell.treasure is not None:
                num_t += 1
                assert 5 <= cell.treasure.value <= 10
    assert num_t == 5

    assert not b.game_over()
    assert b.get_scores() == ''


def find_free(b: Board) -> (int, int):
    for x in range(10):
        for y in range(10):
            if b.game_board[x][y].player is None:
                return x, y

    raise ValueError('board too full')


def test_game_setup():
    b = Board(10, 5, 5, 10, 2)
    i, j = find_free(b)
    b.add_player('1', i, j)
    assert b.game_board[i][j].player.name == '1'
    (_, (x, y)) = b.players['1']
    assert (i, j) == (x, y)

    i, j = find_free(b)
    with pytest.raises(ValueError, match='name already exists'):
        b.add_player('1', i, j)

    with pytest.raises(ValueError, match='x is not in range 0 <= x < n'):
        b.add_player('2', -1, j)

    with pytest.raises(ValueError, match='x is not in range 0 <= x < n'):
        b.add_player('2', 10, j)

    with pytest.raises(ValueError, match='y is not in range 0 <= y < n'):
        b.add_player('2', i, -1)

    with pytest.raises(ValueError, match='y is not in range 0 <= y < n'):
        b.add_player('2', i, 10)

    b.add_player('2', i, j)
    assert b.game_board[i][j].player.name == '2'
    (_, (x, y)) = b.players['2']
    assert (i, j) == (x, y)

    i, j = find_free(b)
    with pytest.raises(ValueError, match='cannot add any more players'):
        b.add_player('3', i, j)


def test_gameplay():
    b = Board(10, 5, 5, 10, 2)

    ttl_val = 0
    for row in b.game_board:
        assert len(row) == 10
        for cell in row:
            if cell.treasure is not None:
                ttl_val += cell.treasure.value

    b.add_player('1', 0, 0)

    with pytest.raises(ValueError, match='already at the top'):
        b.move_player('1', Direction.UP)

    for i in range(9):
        b.move_player('1', Direction.RIGHT)

    with pytest.raises(ValueError, match='already at the right edge'):
        b.move_player('1', Direction.RIGHT)

    for i in range(9):
        b.move_player('1', Direction.DOWN)

    with pytest.raises(ValueError, match='already at the bottom'):
        b.move_player('1', Direction.DOWN)

    for i in range(9):
        b.move_player('1', Direction.LEFT)

    with pytest.raises(ValueError, match='already at the left edge'):
        b.move_player('1', Direction.LEFT)

    for i in range(9):
        b.move_player('1', Direction.UP)

    p = b.game_board[0][0].player
    for i in range(10):
        for j in range(10):
            b.game_board[i][j].remove_player()
            b.game_board[i][j].add_player(p)

    assert p.score == ttl_val
    assert not b.game_over()
