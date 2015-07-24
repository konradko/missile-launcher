from rest_framework import viewsets

from models import Instruction
from serializers import InstructionSerializer


class Instruction(viewsets.ModelViewSet):
    """
    API endpoint that allows instructions to be posted.
    """
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
