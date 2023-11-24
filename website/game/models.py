import pdb

from django.db import models
from django.db.models import Q

# Create your models here.
class Board(models.Model):
    label = models.CharField(max_length=1)
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.IntegerField()

    def __str__(self):
        return f'{self.label} row {self.row}, column {self.col}, value {self.value}'

    @classmethod
    def create_board(cls, r: int, c: int):
        model = cls(label='.', row=r, col=c, value=0)
        return model


class Player(models.Model):
    name = models.CharField(max_length=1)
    row = models.IntegerField()
    col = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return f'{self.name} row {self.row}, column {self.col}, score {self.score}'

    @classmethod
    def create_player(cls, n: str, r: int, c: int):
        model = cls(name=n, row=r, col=c, score=0)
        return model

    #import pdb
    def move_up(self):
        # pdb.set_trace()
        if self.row > 0:
            self.row -= 1
            self.save()
        # Calculate score
        t = Board.objects.get(Q(row=self.row), Q(col=self.col))
        if t.label == '$':
            self.score += 10
            self.save()

    def move_down(self):
        if self.row < 9:
            self.row += 1
            self.save()
        # Calculate score
        t = Board.objects.get(Q(row=self.row), Q(col=self.col))
        if t.label == '$':
            self.score += 10
            self.save()

    def move_left(self):
        if self.col > 0:
            self.col -= 1
            self.save()
        # Calculate score
        t = Board.objects.get(Q(row=self.row), Q(col=self.col))
        if t.label == '$':
            self.score += 10
            self.save()

    def move_right(self):
        if self.col < 9:
            self.col += 1
            self.save()
        # Calculate score
        t = Board.objects.get(Q(row=self.row), Q(col=self.col))
        if t.label == '$':
            self.score += 10
            self.save()

