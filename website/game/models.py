from django.db import models


# Create your models here.
class Board(models.Model):
    label = models.CharField(max_length=1)
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.IntegerField()

    def __str__(self):
        return f'{self.label} row {self.row}, column {self.col}, value {self.val}'


class Player(models.Model):
    name = models.CharField(max_length=1)
    row = models.IntegerField()
    col = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return f'{self.name} row {self.row}, column {self.col}, score {self.score}'