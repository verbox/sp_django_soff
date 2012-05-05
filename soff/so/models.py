from django.db import models

class Table(models.Model):
    clientsCount = models.IntegerField(default=0)
    maxClientsCount = models.IntegerField(default=4)