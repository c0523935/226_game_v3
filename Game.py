from random import randrange
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from struct import pack
from Board import Board, Direction
from View import display, display_scores
from threading import Semaphore, Thread
import struct

class Game:
    def __init__(self):
        self.BUF_SIZE = 1
        self.HOST = ''
        self.PORT = 12345
        self.QUEUE_SIZE = 1

        self.BOARD_SIZE = 10
        self.NUM_TREASURES = 5
        self.MIN_TREASURE = 5
        self.MAX_TREASURE = 10
        self.MAX_PLAYERS = 2
        self.PLAYER1_NAME = '1'
        self.PLAYER2_NAME = '2'

        self.board = Board(self.BOARD_SIZE, self.NUM_TREASURES, self.MIN_TREASURE, self.MAX_TREASURE, self.MAX_PLAYERS)
        self.place_player(self.PLAYER1_NAME)
        self.place_player(self.PLAYER2_NAME)

        self.CMD_MASK = 0b11110000
        self.UP = 0b00100000
        self.LEFT = 0b01000000
        self.RIGHT = 0b01100000
        self.DOWN = 0b00110000
        self.QUIT = 0b10000000
        self.GET = 0b11110000

        self.PLAYER_MASK = 0b00001100
        self.PLAYER1 = 0b0100
        self.PLAYER2 = 0b1000

        self.quitting = False

    def place_player(self, name: str) -> None:
        """
        Place a player with the given name on the board at a free location.

        This method must not be called more than twice, or an infinite loop will result.
        :param name: The name of the player that should be created; must be valid and unique
        """
        while True:
            try:
                self.board.add_player(name, randrange(self.BOARD_SIZE), randrange(self.BOARD_SIZE))
                return
            except ValueError:
                continue

    def generate_score_list(self) -> bytes:
        """
        Generates the list of scores for transmission

        :return: The list of scores
        """
        score_list = self.board.get_score_list()
        reply = pack('!H', score_list[0]) + pack('!H', score_list[1])
        return reply

    def implement_command(self, cmd: int) -> bytes:
        """
        Implement the given command.

        Format is:
        ______00
        4 bits for the command (U is 0010, L is 0100, R is 0110, D is 0011, Q is 1000, G is 1111)
        2 bits for the player (Player 1 is 01 and Player 2 is 10) to whom the movement command applies
        2 0 bits

        :param cmd: The command to implement
        :return: The player 1 and player 2 scores (2 shorts)
        """
        direction = None
        reply = b''

        if self.quitting or self.board.game_over():
            display_scores(self.board)
            display(self.board)
            return self.generate_score_list() + str(self.board).encode()

        match cmd & self.CMD_MASK:
            case self.UP:
                direction = Direction('UP')
            case self.LEFT:
                direction = Direction('LEFT')
            case self.RIGHT:
                direction = Direction('RIGHT')
            case self.DOWN:
                direction = Direction('DOWN')
            case self.QUIT:
                print("Game Over")
                self.quitting = True
                return b''
            case self.GET:
                display_scores(self.board)
                display(self.board)
                reply = str(self.board).encode()
            case _:
                print('Unknown command')
                return b''

        if direction is not None:
            player = cmd & self.PLAYER_MASK
            match player:
                case self.PLAYER1 | self.PLAYER2:
                    try:
                        val = self.board.move_player(self.PLAYER1_NAME if player == self.PLAYER1 else self.PLAYER2_NAME,
                                                     direction)
                    except ValueError as details:
                        print(details)
                        return self.generate_score_list() + str(self.board).encode()
                    else:
                        display_scores(self.board)
                        display(self.board)
                        if val != 0:
                            print(f'+{val}')
                case _:
                    print('Unknown player')
                    return b''

        # return the score and the board
        return self.generate_score_list() + str(self.board).encode()

    def call_server(self, sc: socket, connection_number: int):

        with sc:
            while True:
                data = sc.recv(self.BUF_SIZE)
                print(data, list(data))
                if not data:
                    break
                print(f'Client {connection_number}: {sc.getpeername()} Data: {data.hex()}')
                # result gets the score and the board
                result = self.implement_command(int.from_bytes(data, byteorder='big'))
                if result != b'':
                    print(result, list(result))
                    size = len(result)
                    size_data = struct.pack('!h', size)
                    # sending the size
                    sc.sendall(size_data)
                    # sending score and board
                    sc.sendall(result)

    def start(self) -> None:
        """
        Start the server and process incoming connections.
        """
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind((self.HOST, self.PORT))
            sock.listen(self.QUEUE_SIZE)
            print('Server:', sock.getsockname())

            connexions_counter = 0
            while connexions_counter <= 2:  # only 2 connections
                sc, _ = sock.accept()
                connexions_counter = connexions_counter + 1
                size_data = struct.pack('!H', 1)
                # sending the size
                sc.sendall(size_data)
                byte_value = connexions_counter.to_bytes((connexions_counter.bit_length() + 7) // 8, byteorder='big')
                # sending the player ID
                sc.sendall(byte_value)
                Thread(target=self.call_server, args=(sc, connexions_counter)).start()

            print("Only allow 2 connections, closing the client")










