from django.test import TestCase
from .models import Player, Board
from django.db.models import Q


class PlayerTestCase(TestCase):
    def test_create_players(self):
        self.client.post('/game/create/')

        p1 = Player.objects.get(name='1')
        self.assertEqual(p1.name, '1')

        p2 = Player.objects.get(name='2')
        self.assertEqual(p2.name, '2')

    def test_create_board(self):
        self.client.post('/game/create/')
        tail = 0
        for i in range(10):
            for j in range(10):
                t = Board.objects.get(Q(row=i), Q(col=j))
                tail = tail + 1
        self.assertEqual(tail, 100)

    def test_created_treasures(self):
        self.client.post('/game/create/')
        treasures = 0
        for i in range(10):
            for j in range(10):
                t = Board.objects.get(Q(row=i), Q(col=j))
                if t.label == '$':
                    treasures = treasures + 1
        self.assertEqual(treasures, 5)

    def test_movement_beyond_borders(self):
        self.client.post('/game/create/')
        p = Player.objects.get(name='1')

        """
        Testing UP movement
        """
        print("****************** Testing Up movement ******************")
        print("current row: ", p.row)
        p.row = 0
        p.save()
        print("current row (after assign 0): ", p.row)
        self.client.get('/game/move_player/1/up/')
        p = Player.objects.get(name='1')
        print("current row (after move up): ", p.row)
        self.assertEqual(p.row, 0)

        """
        Testing DOWN movement
        """
        print("****************** Testing Down movement ******************")
        print("\ncurrent row: ", p.row)
        p.row = 9
        p.save()
        print("current row (after assign 9): ", p.row)
        self.client.get('/game/move_player/1/down/')
        p = Player.objects.get(name='1')
        print("current row (after move down): ", p.row)
        self.assertEqual(p.row, 9)

        """
        Testing LEFT movement
        """
        print("****************** Testing Left movement ******************")
        print("\ncurrent col: ", p.col)
        p.col = 0
        p.save()
        print("current col (after assign 0): ", p.col)
        self.client.get('/game/move_player/1/left/')
        p = Player.objects.get(name='1')
        print("current col (after move left): ", p.col)
        self.assertEqual(p.col, 0)

        """
        Testing RIGHT movement
        """
        print("****************** Testing Right movement ******************")
        print("\ncurrent col: ", p.col)
        p.col = 9
        p.save()
        print("current col (after assign 9): ", p.col)
        self.client.get('/game/move_player/1/right/')
        p = Player.objects.get(name='1')
        print("current col (after move right): ", p.col)
        self.assertEqual(p.col, 9)

    def test_update_score(self):
        print("\n************ Testing test_update_score() ****************")
        self.client.post('/game/create/')
        p = Player.objects.get(name='1')
        treasure_x_position = 0
        treasure_y_position = 0

        for i in range(10):
            for j in range(10):
                t = Board.objects.get(Q(row=i), Q(col=j))
                if t.label == '$':
                    treasure_x_position = i
                    treasure_y_position = j

        print("\n\nplayer current position: ", p.row, " ", p.col)
        print("treasure current position: ", treasure_x_position, " ", treasure_y_position)
        print("current score: ", p.score)

        p.row = treasure_x_position + 1
        p.col = treasure_y_position
        p.save()

        print("\nSet player down Treasure\nplayer current position: ", p.row, " ", p.col)
        print("treasure current position: ", treasure_x_position, " ", treasure_y_position)
        print("current score: ", p.score)

        p.move_up()
        p.save()
        p = Player.objects.get(name='1')
        print("\nPlayer cath a Treasure\nplayer current position: ", p.row, " ", p.col)
        print("treasure current position: ", treasure_x_position, " ", treasure_y_position)
        print("current score: ", p.score)
        self.assertEqual(p.score, 10)

    def test_four_movements(self):
        self.client.post('/game/create/')
        p = Player.objects.get(name='1')
        print("****************** Testing Up, Down, Left, Right movements ******************")
        p.row = 5
        p.col = 5
        print("\ninitial row position: ", p.row)
        print("\ninitial col position: ", p.col)
        p.save()

        print(" ##### Moving UP #######")
        self.client.get('/game/move_player/1/up/')
        p = Player.objects.get(name='1')
        print("\ncurrent row: ", p.row)
        print("\ncurrent col: ", p.col)
        self.assertEqual(p.row, 4)

        print(" ##### Moving LEFT #######")
        self.client.get('/game/move_player/1/left/')
        p = Player.objects.get(name='1')
        print("\ncurrent row: ", p.row)
        print("\ncurrent col: ", p.col)
        self.assertEqual(p.col, 4)

        print(" ##### Moving DOWN #######")
        self.client.get('/game/move_player/1/down/')
        p = Player.objects.get(name='1')
        print("\ncurrent row: ", p.row)
        print("\ncurrent col: ", p.col)
        self.assertEqual(p.row, 5)

        print(" ##### Moving RIGHT #######")
        self.client.get('/game/move_player/1/right/')
        p = Player.objects.get(name='1')
        print("\ncurrent row: ", p.row)
        print("\ncurrent col: ", p.col)
        self.assertEqual(p.col, 5)
