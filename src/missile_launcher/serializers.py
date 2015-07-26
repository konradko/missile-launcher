import json

from rest_framework import serializers

from models import Instruction
from . import missle_launcher_device as mld


class JSONSerializerField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class InstructionSerializer(serializers.ModelSerializer):
    commands = JSONSerializerField()

    class Meta:
        model = Instruction
        read_only_fields = ('commands', 'success')

    def validate_commands(self, value):
        commands = value

        for cmd in commands:
            if cmd == mld.MOVES:
                for move in cmd:
                    if move not in mld.commands:
                        raise serializers.ValidationError("Invalid command")
            elif cmd == mld.MOVE:
                if not cmd.get('x_distance') and cmd.get('y_distance'):
                    raise serializers.ValidationError(
                        "Invalid command: x_distance and y_distance required"
                    )
            elif cmd == mld.MOVE_TO:
                if not cmd.get('x_percentage') and cmd.get('y_percentage'):
                    raise serializers.ValidationError(
                        "Invalid command: "
                        "x_percentage and y_percentage required"
                    )
            else:
                raise serializers.ValidationError("Invalid command")

        return commands

    def execute_commands(self, commands):
        success = True
        for cmd in commands:
            try:
                mld.execute(cmd)
            except:
                success = False
                break
        return success

    def create(self, validated_data):
        commands = validated_data['commands']
        json_commands = json.dumps(commands)
        success = True
        if mld.MOVES in commands:
            success = self.execute_commands(commands[mld.MOVES])
            commands.pop(mld.MOVES)

        if success is True:
            self.execute_commands(commands)

        instruction = Instruction(
            commands=json_commands, success=success
        )
        instruction.save()

        return instruction
