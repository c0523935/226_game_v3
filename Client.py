#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import struct

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345


class Client:
    player = None

    def call_client(self):
        """
        This function set the connection with the server
        :return:
        """

        def receive(sc, size):
            """
            This function get the data receive en return its size
            :param sc:
            :param size:
            :return: an int value (size)
            """
            data = b''
            while len(data) < size:
                curr_data = sc.recv(size - len(data))
                if curr_data == b'':
                    return data

                data += curr_data

            return data

        with socket(AF_INET, SOCK_STREAM) as sock:

            sock.connect((HOST, PORT))
            print('Client:', sock.getsockname())
            # getting the size
            reply_size = receive(sock, 2)
            # getting the player ID
            player = receive(sock, 1)
            # showing the player ID
            print('Player: ', player)

            while True:
                # dictionary of possible movements
                movements_1 = {'U': 0x24, 'D': 0x34, 'R': 0x64, 'L': 0x44, 'Q': 0x84}
                movements_2 = {'U': 0x28, 'D': 0x38, 'R': 0x68, 'L': 0x48, 'Q': 0x88}
                # ask for a movement
                command = input("Input (U, D, R, L, Q): ")
                command = command.upper()

                if player == b'\x01':
                    if command in movements_1:
                        valor = movements_1[command]
                if player == b'\x02':
                    if command in movements_2:
                        valor = movements_2[command]
                if command == 'Q':
                    break

                data_to_send = bytes([valor])
                # sending the movement
                sock.sendall(data_to_send)
                # getting the size
                reply_size = receive(sock, 2)
                # getting the score and board
                reply_size_int = int.from_bytes(reply_size, byteorder='big')
                reply = sock.recv(reply_size_int)

                # Split scores and board
                scores = reply[:4]  # the first 4 bytes are the score
                board_data = reply[4:]  # the rest is the board
                decoded_scores = struct.unpack('!HH', scores)  # decode de score
                decoded_board = board_data.decode()
                # show scores and board
                print(f"Player 1 Score: {decoded_scores[0]}")
                print(f"Player 2 Score: {decoded_scores[1]}")
                print("Board:")
                print(decoded_board)


c = Client()
c.call_client()