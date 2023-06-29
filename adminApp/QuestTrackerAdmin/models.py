from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    event_id = models.IntegerField()

    def __str__(self):
        return self.username


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name

class Progress(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    objective_id = models.IntegerField()
    current_progress = models.IntegerField()

    def __str__(self):
        return f"Player: {self.player.username}, Objective ID: {self.objective_id}"

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coin_balance = models.IntegerField()

    def __str__(self):
        return f"Player: {self.user.username}, Coin Balance: {self.coin_balance}"
