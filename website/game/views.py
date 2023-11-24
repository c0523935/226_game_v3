from django.shortcuts import render
from django.http import HttpResponse
from .models import Player
from .models import Board
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
import random


def index(request):
    full_html = '<div style="text-align: center; margin: 20px;">'
    board_to_print = ""
    for i in range(10):
        for j in range(10):
            # Board.create_board(i, j).save()
            t = Board.objects.get(Q(row=i), Q(col=j))

            board_to_print = "\t" + board_to_print + str(t.label) + "\t"

        board_to_print = board_to_print + "<br>"

    # ADD 2 player links
    choose_player_html = (
        '<a href="/game/display/1">Player 1</a><br>'
        '<a href="/game/display/2">Player 2</a>'
    )
    player1 = Player.objects.get(name='1')
    player2 = Player.objects.get(name='2')
    score_html = (
        f'<p>Player 1 Score: {player1.score}</p>'
        f'<p>Player 2 Score: {player2.score}</p>'
    )
    # Combine all
    full_html += board_to_print + choose_player_html + score_html
    full_html += '</div>'
    return HttpResponse(full_html)


def board(request):
    if not Board.objects.exists():
        board_to_print = create()

    # return HttpResponse('Board 10x10, 5 Treasures and 2 players were created')
    return index(request)

@transaction.atomic
def create():

    board_to_print = ""

    """
        ************* Create Random Treasures *************
    """
    treasure_positions = set()
    tre = [[None] * 2 for _ in range(5)]
    t_cant = 0
    while t_cant < 5:
        random_number_x = random.randint(0,9)
        random_number_y = random.randint(0, 9)
        # Check if the position is already in the set()
        while (random_number_x, random_number_y) in treasure_positions:
            random_number_x = random.randint(0, 9)
            random_number_y = random.randint(0, 9)

        # Add the new position to the set()
        treasure_positions.add((random_number_x, random_number_y))

        tre[t_cant][0] = random_number_x
        tre[t_cant][1] = random_number_y
        t_cant = t_cant + 1

    """
        ************* Create 2 random players *************
    """
    player_positions = set()
    # player 1
    random_x_1 = random.randint(0, 9)
    random_y_1 = random.randint(0, 9)
    # Check if the position is already use for a Treasure
    while (random_x_1, random_y_1) in treasure_positions:
        random_x_1 = random.randint(0, 9)
        random_y_1 = random.randint(0, 9)
    # Add the player 1 position to the set()
    player_positions.add((random_x_1, random_y_1))
    # player 2
    random_x_2 = random.randint(0, 9)
    random_y_2 = random.randint(0, 9)
    # Check if the position is already use for a Treasure and the previous set() from player 1
    while (random_x_2, random_y_2) in treasure_positions or (random_x_2, random_y_2) in player_positions:
        random_x_2 = random.randint(0, 9)
        random_y_2 = random.randint(0, 9)
    # Add the player 2 position to the set()
    player_positions.add((random_x_2, random_y_2))

    Player.create_player('1' , random_x_1, random_y_1).save()
    Player.create_player('2', random_x_2, random_y_2).save()
    p1 = Player.objects.get(Q(row=random_x_1), Q(col=random_y_1))
    p2 = Player.objects.get(Q(row=random_x_2), Q(col=random_y_2))
    """
            ************* Create the board *************
    """

    for i in range(10):
        for j in range(10):
            Board.create_board(i, j).save()
            t = Board.objects.get(Q(row=i), Q(col=j))

            for ind in range(5):
                if tre[ind][0] == i and tre[ind][1] == j:
                    t.label = '$'

            if random_x_1 == i and random_y_1 == j:
                t.label = p1.name

            if random_x_2 == i and random_y_2 == j:
                t.label = p2.name
            t.save()
            board_to_print = "\t" + board_to_print + str(t.label) + "\t"

        board_to_print = board_to_print + "<br>"

    return board_to_print


@transaction.atomic
def display1(request):
    print('llamando a display1')
    board_to_print = ""
    for i in range(10):
        for j in range(10):
            t = Board.objects.get(Q(row=i), Q(col=j))
            board_to_print += "\t" + str(t.label) + "\t"
        board_to_print += "<br>"
    # Get data from players
    player1 = Player.objects.get(name='1')
    player2 = Player.objects.get(name='2')

    # Build HTML scores
    score_html = (
        f'<p>Player 1 Score: {player1.score}</p>'
        f'<p>Player 2 Score: {player2.score}</p>'
    )

    # Build the context with the components
    context = {
        'board_to_print': board_to_print,
        'score_html': score_html,
        'player_id': 1
    }

    return render(request, 'game/game.html', context)


@transaction.atomic
def display2(request):
    print('llamando a display2')
    board_to_print = ""
    for i in range(10):
        for j in range(10):
            t = Board.objects.get(Q(row=i), Q(col=j))
            board_to_print += "\t" + str(t.label) + "\t"
        board_to_print += "<br>"
    # Get data from players
    player1 = Player.objects.get(name='1')
    player2 = Player.objects.get(name='2')

    # Build HTML scores
    score_html = (
        f'<p>Player 1 Score: {player1.score}</p>'
        f'<p>Player 2 Score: {player2.score}</p>'
    )

    # Build the context with the components
    context = {
        'board_to_print': board_to_print,
        'score_html': score_html,
        'player_id': 2
    }

    return render(request, 'game/game.html', context)


@transaction.atomic
def move_player(request, player_id, direction):
    # print("player id", player_id, "direction ", direction)
    player = Player.objects.get(name=player_id)

    # Calculate the possible position
    new_row, new_col = player.row, player.col
    if direction == 'up' and player.row > 0:
        new_row -= 1
    elif direction == 'down' and player.row < 9:
        new_row += 1
    elif direction == 'left' and player.col > 0:
        new_col -= 1
    elif direction == 'right' and player.col < 9:
        new_col += 1

    # Check if the new position is occupied by another player
    if Player.objects.filter(row=new_row, col=new_col).exclude(name=player_id).exists():

        return HttpResponseRedirect(reverse('display1' if player_id == '1' else 'display2'))

    # Find and update the label of the previous position to '.'
    Board.objects.filter(row=player.row, col=player.col).update(label='.')
    # Move the player to the new position if is available
    if direction == 'up':
        player.move_up()
    if direction == 'down':
        player.move_down()
    if direction == 'left':
        player.move_left()
    if direction == 'right':
        player.move_right()

    # Calculate score
    t = Board.objects.get(Q(row=player.row), Q(col=player.col))
    if t.label == '$':
        player.score += 10
        player.save()
        print('Found a treasure: ', player.score)

    # Capture the initial position of the player
    initial_row, initial_col = player.row, player.col

    # Find and update the label of the previous tail board
    try:
        previous_board_position = Board.objects.get(row=initial_row, col=initial_col)
        previous_board_position.label = '.'
        previous_board_position.save()
    except Board.DoesNotExist:
        pass

    # Find and update the label of the new tail board
    try:
        new_board_position = Board.objects.get(row=player.row, col=player.col)
        new_board_position.label = player.name
        new_board_position.save()
    except Board.DoesNotExist:

        pass

    if player_id == '1':
        return HttpResponseRedirect(reverse('display1'))
    elif player_id == '2':
        print('update screen player 2')
        return HttpResponseRedirect(reverse('display2'))
























  # full_html = '<div style="text-align: center; margin: 20px;">'
    # board_to_print = ""
    # for i in range(10):
    #     for j in range(10):
    #         # Board.create_board(i, j).save()
    #         t = Board.objects.get(Q(row=i), Q(col=j))
    #
    #         board_to_print = "\t" + board_to_print + str(t.label) + "\t"
    #
    #     board_to_print = board_to_print + "<br>"
    # # Botones de dirección
    # direction_buttons_html = (
    #     '<div style="text-align: center; margin: 20px;">'
    #     '<button style="margin: 10px;">↑</button><br>'
    #     '<button style="margin: 10px;">←</button>'
    #     '<span style="display: inline-block; width: 20px; text-align: center;">2</span>'
    #     '<button style="margin: 10px;">→</button><br>'
    #     '<button style="margin: 10px;">↓</button>'
    #     '</div>'
    # )
    # player1 = Player.objects.get(name='1')
    # player2 = Player.objects.get(name='2')
    # score_html = (
    #
    #     f'<p>Player 1 Score: {player1.score}</p>'
    #     f'<p>Player 2 Score: {player2.score}</p>'
    #
    # )
    # # Combine all
    # full_html += board_to_print + direction_buttons_html + score_html
    # full_html += '</div>'
    # return HttpResponse(full_html)