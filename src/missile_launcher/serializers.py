from rest_framework import serializers

from models import Instruction

from missile_launcher_driver import MissileLauncherDriver
from . import missle_launcher_device


class InstructionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instruction
        fields = ('commands')
        read_only_fields = ('commands')

    def validate_commands(self, value):
        commands = value.split(",")
        if any(cmd not in MissileLauncherDriver.commands for cmd in commands):
            raise serializers.ValidationError("Invalid commands")
        return commands

    def create(self, validated_data):
        success = True
        commands = validated_data['commands']
        for command in commands:
            try:
                missle_launcher_device.send_cmd(command)
            except:
                success = False
                break

        instruction = Instruction(commands=",".join(commands), success=success)
        instruction.save()

        return instruction
