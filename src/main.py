from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Iterable
from grammar import build_grammar
from enum import Enum, auto
from parsimonious.nodes import NodeVisitor
from commands.move import *
from commands.fullscreen import *
from commands.exec import *
import os

class BindOption(Enum): 
    RELEASE = auto()
    BORDER = auto()
    WHOLE_WINDOW = auto()
    EXCLUDE_TITLEBAR = auto()

    @staticmethod
    def from_str(s: str):
        if s == "--release":
            return BindOption.RELEASE
        elif s == "--border":
            return BindOption.BORDER
        elif s == "--whole-window":
            return BindOption.WHOLE_WINDOW
        elif s == "--exclude-titlebar":
            return BindOption.EXCLUDE_TITLEBAR
        else:
            raise ValueError(f"Expected one of (--release, --border, --whole-window, --exclude-titlebar), got {s}")

    def __str__(self):
        return '--' + self.name.lower().replace('_', '-')

class Separator(Enum):
    SEMICOLON = auto()
    COMMA = auto()

class I3Binding(object):
    def __init__(self,
                 keyword: str,
                 bind_options0: List[BindOption],
                 key: str,
                 bind_options1: List[BindOption],
                 commands: List[Command],
                 separators: List[Separator],
                 spacing: Iterable[str] = all_spaces):
        self.keyword = keyword
        self.bind_options0 = bind_options0
        self.key = key
        self.bind_options1 = bind_options1
        self.commands = commands
        self.separators = separators
        self.spacing = spacing
    
    def __str__(self):
        s = self.keyword
        space_index = 0
        for bind_option in self.bind_options0:
            s += self.spacing[space_index]
            space_index += 1
            s += str(bind_option)
        
        s += self.spacing[space_index]
        space_index += 1
        s += self.key
        for bind_option in self.bind_options1:
            s += self.spacing[space_index]
            space_index += 1
            s += str(bind_option)
        
        s += self.spacing[space_index]
        space_index += 1
        for separators_index, command in enumerate(self.commands):
            s += str(command)
            # We don't add a space or separator for the last command
            if separators_index < len(self.commands) - 1:
                s += self.spacing[space_index]
                space_index += 1
                s += self.separators[separators_index]
                s += self.spacing[space_index]
                space_index += 1

        
        return s


class I3ConfigVisitor(NodeVisitor):

    def visit_bind_statement(self, node, bind_statement):
        # bind_option0 and bind_option1 are either an 
        # empty node or a list of list of strings including the prepending space
        # TODO: Return an object instead
        bind_options0 = []
        bind_options1 = []
        keyword, space_bind_option0, space0, key, space_bind_option1, space1, bind_actions = bind_statement
        keyword = keyword[0].text
        key = key.text
        commands = bind_actions["commands"]
        spacing = bind_actions["spacing"]
        separators = bind_actions["separators"]
        spacing.insert(0, space1)
        if type(space_bind_option1) == list:
            for space_bind_option in space_bind_option1:
                bind_space, bind_option = space_bind_option
                spacing.insert(0, bind_space)
                bind_option = BindOption.from_str(bind_option)
                bind_options1.append(bind_option)
        spacing.insert(0, space0)
        if type(space_bind_option0) == list:
            for space_bind_option in space_bind_option0:
                bind_space, bind_option = space_bind_option
                spacing.insert(0, bind_space)
                bind_option = BindOption.from_str(bind_option)
                bind_options0.append(bind_option)
        
        
        binding = I3Binding(keyword, bind_options0, key, bind_options1, commands, separators, spacing)
        with open("output.config", 'a') as out:
            out.write(str(binding) + '\n')
        return binding

    def visit_fullscreen_command(self, node, fullscreen_command):
        # space_fullscreen_command is a list containing the spaces
        # and the object returned by visit_fullscreen_xxxx
        _, space_fullscreen_command = fullscreen_command
        if type(space_fullscreen_command) == list:
            space_fullscreen_command, = space_fullscreen_command
            space, fullscreen_command = space_fullscreen_command
            fullscreen_command, = fullscreen_command
            fullscreen_command._add_spacing_reversed(space)
        else:
            fullscreen_command = FullscreenCommand(FullscreenArgument.NONE, is_global=False, spacing=[])
        return fullscreen_command

    def visit_fullscreen_mode(self, node, fullscreen_mode):
        spacing = []
        is_global = False
        enable_or_toggle, space_global = fullscreen_mode
        enable_or_toggle = enable_or_toggle[0].text
        if type(space_global) == list:
            space_global, = space_global
            space, _ = space_global
            spacing.append(space)
            is_global = True
        
        fullscreen_arg = FullscreenArgument.from_string(enable_or_toggle)
        fullscreen_command = FullscreenCommand(fullscreen_arg, is_global, spacing)
        return fullscreen_command

    def visit_fullscreen_disable(self, node, fullscreen_disable):
        return FullscreenCommand(FullscreenArgument.DISABLE, spacing=[])
    
    def visit_fullscreen_global(self, node, fullscreen_global):
        return FullscreenCommand(FullscreenArgument.NONE, is_global=True, spacing=[])

    def visit_statement_no_line(self, node, statement_no_line):
        statement_no_line, = statement_no_line
        if type(statement_no_line) == ExecCommand:
            with open("output.config", 'a') as output:
                output.write(f"{str(statement_no_line)}\n")

    def visit_exec_command(self, node, exec_command):
        _, space, command = exec_command
        return ExecCommand(command, spacing=[space])

    def visit_bind_actions(self, node, bind_actions):
        bind_actions, = bind_actions
        if type(bind_actions) == list:
            bind_action, space0, separator, space1, bind_actions = bind_actions
            if type(space0) == list:
                space0, = space0
            else:
                space0 = space0.text
            separator, = separator
            separator = separator.text
            if type(space1) == list:
                space1, = space1
            else:
                space1 = space1.text
            # If bind_actions is a list than this is the first
            # in the sequence of bind_actions so we initalize the dict
            if type(bind_actions) == list:
                bind_actions = {
                    "spacing": [],
                    "separators": [],
                    "commands": [bind_actions[0]]
                }
            bind_actions["commands"].insert(0, bind_action)
            bind_actions["spacing"].insert(0, space1)
            bind_actions["spacing"].insert(0, space0)
            bind_actions["separators"].insert(0, separator)
            return bind_actions
        else:
            return {
                "spacing": [],
                "separators": [],
                "commands": [bind_actions]
            }

    def visit_bind_action(self, node, bind_action):
        bind_action, = bind_action
        return bind_action

    def visit_i3_move_command(self, node, i3_move_command):
        # _: literal "move"
        # space_move_targets: list of lists with 2 elements each containing [space, <the move target>]
        # space1: some amount of space
        # move_tail: the move tail as returned by the relavent visit_move_xxxx method
        _, space_move_targets, space1, move_tail = i3_move_command
        move_command, = move_tail
        move_command._add_spacing_reversed(space1)
        if type(space_move_targets) == list:
            # Iterate backwards through space_move_targets because we
            # add them (and spacing) to the beginning of the list
            for space_move_target in reversed(space_move_targets):
                space, move_target = space_move_target
                move_target, = move_target
                move_target = move_target.text
                move_command._add_spacing_reversed(space)
                move_command.move_targets.insert(0, move_target) 
        
        return move_command

    def visit_move_workspace(self, node, move_workspace) -> MoveWorkspace:
        _, space, destination = move_workspace
        destination, = destination
        if type(destination) == MoveWorkspaceTo:
            destination._add_spacing_reversed(space)
            return destination
        else:
            destination = destination.text
            move_command = MoveWorkspace(destination)
            move_command._add_spacing_reversed(space)
            return move_command

    def visit_move_to_output(self, node, move_to_output):
        _, space, word = move_to_output
        word = word.text
        spacing = [space]
        move_command = MoveToOutput(word, spacing=spacing)
        return move_command

    def visit_move_workspace_to(self, node, move_workspace_to) -> MoveWorkspaceTo:
        _, space0, _, space1, output_name = move_workspace_to
        output_name = output_name.text
        spacing = [space0, space1]
        move_command = MoveWorkspaceTo(output_name, spacing=spacing)
        return move_command

    def visit_move_to_mark(self, node, move_to_mark) -> MoveToMark:
        _, space, mark_name = move_to_mark
        mark_name = mark_name.text
        move_command = MoveToMark(mark_name)
        move_command._add_spacing_reversed(space)
        return move_command
    
    def visit_move_direction(self, node, move_direction):
        move_command = None
        direction, space_measurement = move_direction
        direction, = direction
        direction = direction.text
        direction = Direction.from_string(direction)
        if type(space_measurement) == list:
            space_measurement, = space_measurement
            space, measurement = space_measurement
            space = [space]
            move_command = MoveDirection(direction, spacing=space, measurement=measurement)
        else:
            move_command = MoveDirection(direction)

        return move_command

    def visit_move_to_position(self, node, move_to_position):
        _, space, move_position = move_to_position
        space = [space]
        move_command = MoveToPosition(move_position, spacing=space)
        return move_command

    def visit_move_to_absolute_position(self, node, move_to_absolute_position):
        _, space, move_to_position = move_to_absolute_position

        spacing = [space]
        # This could be trouble if move_to_position.spacing is an ifinite iterator
        # but that shouldn't be a concern because we always override it
        spacing.extend(move_to_position.spacing)
        return MoveToAbsolutePosition(move_to_position.position, spacing=spacing)

    
    def visit_move_position(self, node, move_position):
        position, = move_position
        if type(position) == list:
            return I3MovePosition(I3MovePositionKind.MEASUREMENT_PAIR, position)
        else:
            return I3MovePosition(I3MovePositionKind[position.text.upper()])

    def visit_axiomatic_measurement(self, node, axiomatic_measurement):
        number = 0
        space = ''
        unit = Unit.NONE
        number, space_unit = axiomatic_measurement
        number = int(number.text)
        if type(space_unit) == list:
            space_unit, = space_unit
            space, unit = space_unit
            if type(space) == list:
                space, = space
            else:
                space = space.text
            unit, = unit
            unit = unit.text
            unit = Unit.from_string(unit)

        space = [space]
        measurement = Measurement(number, spacing=space, unit=unit)
        return measurement
        
    def visit_bind_option(self, node, bind_option):
        return node.text

    def visit_any_chars(self, node, any_chars):
        return node.text
    
    def visit_space(self, node, space):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


if __name__ == "__main__":
    g = build_grammar()
    for test_file in os.listdir("tests"):
        if os.path.exists("output.config"):
            os.remove("output.config")
        test_file = "tests/" + test_file 
        with open(test_file, 'r') as config_file:
            config_text = config_file.read() 
        ast = g.parse(config_text)
        I3ConfigVisitor().visit(ast)
        with open(test_file, 'r') as original:
            with open("output.config", 'r') as output:
                for original_line, output_line in zip(original, output):
                    if original_line != output_line:
                        print(f"Original: '{original_line}'")
                        print(f"Test:     '{output_line}'")
        