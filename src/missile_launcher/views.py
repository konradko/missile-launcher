from rest_framework import viewsets
from rest_framework.parsers import JSONParser

import models
from serializers import InstructionSerializer


class Instruction(viewsets.ModelViewSet):
    """
    API endpoint that allows instructions to be posted.
    """
    parser_classes = (JSONParser,)
    queryset = models.Instruction.objects.all()
    serializer_class = InstructionSerializer
