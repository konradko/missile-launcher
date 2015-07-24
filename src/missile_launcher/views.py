from rest_framework import viewsets

import models
from serializers import InstructionSerializer


class Instruction(viewsets.ModelViewSet):
    """
    API endpoint that allows instructions to be posted.
    """
    queryset = models.Instruction.objects.all()
    serializer_class = InstructionSerializer
