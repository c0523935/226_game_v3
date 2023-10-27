#!/usr/bin/python3.11

PORT = 12345

CMD_MASK = 0b11110000
UP = 0b00100000
LEFT = 0b01000000
RIGHT = 0b01100000
DOWN = 0b00110000
QUIT = 0b10000000
GET = 0b11110000

PLAYER_MASK = 0b00001100
PLAYER1 = 0b0100
PLAYER2 = 0b1000
PLAYER1_NAME = '1'
PLAYER2_NAME = '2'

ERROR = b'E'
OK = b'O'