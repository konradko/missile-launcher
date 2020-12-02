from django.db import models


class Instruction(models.Model):
    commands = models.TextField()
    success = models.BooleanField()
