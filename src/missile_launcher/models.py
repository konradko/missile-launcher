from django.db import models


class Instruction(models.Model):
    commands = models.TextField(blank=False)
    success = models.BooleanField(null=False)
