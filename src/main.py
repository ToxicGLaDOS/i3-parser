from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Iterable
from grammar import build_grammar
from enum import Enum, auto
from parsimonious.nodes import NodeVisitor
from variable import *
from commands.move import *
from commands.fullscreen import *
from commands.exec import *
from commands.mode import *
from commands.focus import *
from commands.kill import *
from commands.layout import *
from commands.direct import *
from commands.split import *
from commands.floating import *
from commands.sticky import *
from commands.workspace import *
from commands.resize import *
from commands.scratchpad import *
from commands.border import *
from commands.command_set import *
from statements.comment import *
from statements.workspace import *
from statements.empty import *
from statements.set import *
from statements.font import *
from statements.floating_modifier import *
from statements.assign import *
from statements.binding import *
import os


class I3ConfigVisitor(NodeVisitor):

    def visit_line(self, node, line):
        space_optional, line = line
        space = ''
        line, = line
        if type(space_optional) == list:
            space, = space_optional
        with open("output.config", 'a') as out:
            out.write(space + str(line) + '\n')
        return line

    def visit_statement(self, node, statement):
        statement, _ = statement
        return statement

    def visit_binding_statement(self, node, binding_statement):
        # bind_option0 and bind_option1 are either an 
        # empty node or a list of list of strings including the prepending space
        # TODO: Return an object instead
        bind_options0 = []
        bind_options1 = []
        spacing = []
        keyword, space_bind_option0, space0, key, space_bind_option1, space1, commands = binding_statement
        keyword = keyword[0].text
        key = key
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
        
        
        binding = BindingStatement(keyword, bind_options0, key, bind_options1, commands, spacing=spacing)
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

    def visit_direct_command(self, node, direct_command):
        direct_command, = direct_command
        return DirectCommand(DirectCommandArgument.from_string(direct_command.text))

    def visit_split_command(self, node, split_command):
        _, space, split_direction = split_command
        return SplitCommand(split_direction, spacing=[space])

    def visit_split_direction(self, node, split_direction):
        split_direction, = split_direction
        return SplitDirection.from_string(split_direction.text)

    def visit_floating_command(self, node, floating_command):
        _, space, enableDisableToggle = floating_command
        return FloatingCommand(enableDisableToggle, spacing=[space])

    def visit_enable_disable_toggle(self, node, enable_disable_toggle):
        enable_disable_toggle, = enable_disable_toggle
        return EnableDisableToggle.from_string(enable_disable_toggle.text)

    def visit_sticky_command(self, node, sticky_command):
        _, space, enableDisableToggle = sticky_command
        return StickyCommand(enableDisableToggle, spacing=[space])

    def visit_workspace_command(self, node, workspace_command):
        _, space, workspace_command, = workspace_command
        workspace_command._add_spacing_reversed(space)
        return workspace_command

    def visit_workspace_params(self, node, workspace_params):
        workspace_params, = workspace_params
        if isinstance(workspace_params, WorkspaceCommand):
            return workspace_params
        # In this case it matched the "rest" part in the grammer
        else:
            workspace_label = workspace_params
            return WorkspaceLabeled(workspace_label, spacing=[])

    def visit_workspace_direction(self, node, workspace_direction):
        workspace_direction, = workspace_direction
        return WorkspaceDirection(WorkspaceDirectionOption.from_string(workspace_direction.text), spacing=[])

    def visit_workspace_number(self, node, workspace_number):
        _, space, workspace_number, = workspace_number
        return WorkspaceNumber(int(workspace_number.text), spacing=[space])

    def visit_workspace_back_and_forth(self, node, workspace_back_and_forth):
        workspace_back_and_forth, = workspace_back_and_forth
        return WorkspaceBackAndForth(spacing=[])

    def visit_resize_command(self, node, resize_command):
        _, space, resize_command, = resize_command
        resize_command, = resize_command
        resize_command._add_spacing_reversed(space)
        return resize_command

    def visit_resize_absolute(self, node, resize_absolute):
        _, space0, resize_type = resize_absolute

        resize_type, = resize_type
        label = resize_type[0]
        spacing = [space0]
        if label == "width" or label == "height":
            label, keyword_explicit, space1, measurement = resize_type
            if space1:
                spacing.append(space1)
            if label == "width": 
                return ResizeAbsolute(width_explicit=keyword_explicit, width_measurement=measurement, spacing=spacing)
            else:
                return ResizeAbsolute(height_explicit=keyword_explicit, height_measurement=measurement, spacing=spacing)
        else:
            label, resize_width, space2, resize_height = resize_type
            _, width_explicit, space1, width_measurement = resize_width
            _, height_explicit, space3, height_measurement = resize_height
            if space1:
                spacing.append(space1)
            spacing.append(space2)
            if space3:
                spacing.append(space3)
            return ResizeAbsolute(width_explicit=width_explicit, width_measurement=width_measurement, height_explicit=height_explicit, height_measurement=height_measurement, spacing=spacing)
   
    def visit_resize_width(self, node, resize_width) ->  tuple[str, bool, str, Measurement]:
        """
        str: Just a label so we know whether it's height or width in visit_resize_absolute
        bool: Whether or not the word "width" was used
        str: the space between "width" and the measurement (empty string if "width" was not specified)
        Measurement: a measurement object representing the measurement
        """
        width_space_optional, measurement, = resize_width
        if type(width_space_optional) == list:
            width_space_optional, = width_space_optional
            _, space, = width_space_optional
            return ("width", True, space, measurement)
        else:
            return ("width", False, "", measurement)
 
    def visit_resize_height(self, node, resize_height) -> tuple[str, bool, str, Measurement]:
        """
        str: Just a label so we know whether it's height or width in visit_resize_absolute
        bool: Whether or not the word "height" was used
        str: the space between "height" and the measurement (empty string if "height" was not specified)
        Measurement: a measurement object representing the measurement
        """
        height_space_optional, measurement, = resize_height
        if type(height_space_optional) == list:
            height_space_optional, = height_space_optional
            _, space, = height_space_optional
            return ("height", True, space, measurement)
        else:
            return ("height", False, "", measurement)

    def visit_resize_both(self, node, resize_both) -> tuple[str, tuple[str, bool, str, Measurement], str, tuple[str, bool, str, Measurement]]:
        resize_width, space, resize_height = resize_both
        return ("both", resize_width, space, resize_height)

    def visit_resize_relative(self, node, resize_relative):
        shrink_grow, space0, direction, measurement_optionals = resize_relative
        shrink_grow, = shrink_grow
        shrink_grow = shrink_grow.text
        resize_relative_kind = ResizeRelativeKind.from_string(shrink_grow)

        if type(measurement_optionals) == list:
            measurement_optionals, = measurement_optionals
            space1, pixel_measurement, measurement_optionals = measurement_optionals
            # The first measurement must be in pixels or left empty (which is interpretted as pixels in i3)
            # This could be solved in the grammar, but it's more trouble than it worth imo
            assert pixel_measurement.units == Unit.PX or pixel_measurement.units == Unit.NONE
            if type(measurement_optionals) == list:
                measurement_optionals, = measurement_optionals
                space2, _, space3, percentage_measurement = measurement_optionals
                # Similar to the comment above this measurement must be in ppt or left empty (which is interpretted as ppt in i3)
                assert percentage_measurement.units == Unit.PPT or pixel_measurement.units == Unit.NONE
                return ResizeRelative(resize_relative_kind, direction, pixel_measurement, percentage_measurement, spacing=[space0, space1, space2, space3])
            else:
                return ResizeRelative(resize_relative_kind, direction, pixel_measurement, spacing=[space0, space1])
        else:
            return ResizeRelative(resize_relative_kind, direction, spacing=[space0])

    def visit_resize_direction(self, node, resize_direction):
        resize_direction, = resize_direction
        return ResizeDirection.from_string(resize_direction.text)

    def visit_statement_no_line(self, node, statement_no_line):
        statement_no_line, = statement_no_line
        return statement_no_line

    def visit_scratchpad_command(self, node, scratchpad_command):
        _, space, _, = scratchpad_command
        return ScratchpadCommand(spacing=[space])

    def visit_border_command(self, node, border_command):
        _, space, border_argument, = border_command
        return BorderCommand(border_argument, spacing=[space])

    def visit_border_tail(self, node, border_tail):
        border_tail, = border_tail
        return border_tail

    def visit_border_no_arg(self, node, border_no_arg):
        border_no_arg, = border_no_arg
        style = BorderStyle.from_string(border_no_arg.text)
        return BorderArgument(style, spacing=[])

    def visit_border_arg(self, node, border_arg):
        border_arg, space_number = border_arg
        border_arg, = border_arg
        spacing = []
        number = None
        if type(space_number) == list:
            space_number, = space_number
            space, number = space_number
            spacing.append(space)
            number = int(number.text)


        style = BorderStyle.from_string(border_arg.text)
        return BorderArgument(style, number, spacing=spacing)

    def visit_workspace_statement(self, node, workspace_statement):
        _, space0, workspace_name, space1, _, space2, output_name = workspace_statement
        return WorkspaceStatement(workspace_name, output_name, spacing=[space0, space1, space2])

    def visit_set_statement(self, node, set_statement):
        _, space0, variable_name, space1, value = set_statement
        return SetStatement(variable_name, value, spacing=[space0, space1])

    def visit_font_statement(self, node, font_statement):
        _, space, font_name = font_statement
        return FontStatement(font_name, spacing=[space])

    def visit_floating_modifier_statement(self, node, floating_modifier_statement):
        _, modifiers = floating_modifier_statement
        if type(modifiers) == list:
            spacing = []
            pluses = []
            mod_key_or_vars = []
            for modifier in modifiers:
                space0, mod_key_or_var, space_plus_optional = modifier
                spacing.append(space0)
                mod_key_or_var, = mod_key_or_var
                mod_key_or_vars.append(mod_key_or_var)
                if type(space_plus_optional) == list:
                    space_plus_optional, = space_plus_optional
                    space, _ = space_plus_optional
                    spacing.append(space)
                    pluses.append(True)
                else:
                    pluses.append(False)
            return FloatingModifierStatement(mod_key_or_vars, pluses=pluses, spacing=spacing)
        # No arguments to floating_modifier statement
        else:
            return FloatingModifierStatement([], spacing=[])

    def visit_modifier_key(self, node, modifier_key):
        modifier_key, = modifier_key
        return ModifierKey.from_string(modifier_key.text)

    def visit_assign_statement(self, node, assign_statement):
        _, space0, criteria_set, space1, assign_tail = assign_statement
        spacing = [space0, space1]
        has_arrow, assign_option, target, tail_spacing = assign_tail
        spacing.extend(tail_spacing)
        return AssignStatement(criteria_set, assign_option, target, has_arrow=has_arrow, spacing=spacing)

    def visit_assign_tail(self, node, assign_tail):
        """
        Returns a list containing
        bool: whether the arrow was used
        AssignOption: the AssignOption that was specified
        str: target of the assignment option. A workspace name or output name Ex: HDMI-0, 10, DP-0
        list[str]: spacing
        """
        arrow_space_optional, assign_option_space, target = assign_tail
        return_list = []
        spacing = []
        if type(arrow_space_optional) == list:
            arrow_space_optional, = arrow_space_optional
            _, space0 = arrow_space_optional
            spacing.append(space0)
            return_list.append(True)
        else:
            return_list.append(False)
        if type(assign_option_space) == list:
            assign_option_space, = assign_option_space
            assign_option, space1 = assign_option_space
            assign_option, = assign_option
            spacing.append(space1)
            return_list.append(AssignOption.from_string(assign_option.text))
        else:
            return_list.append(AssignOption.NONE)
        return_list.append(target)
        return_list.append(spacing)

        return return_list

    def visit_criteria_set(self, node, criteria_set):
        _, criteria0, space_criteria, _ = criteria_set
        spacing = []
        criteria_list = [criteria0]
        if type(space_criteria) == list:
            for space, criteria in space_criteria:
                spacing.append(space)
                criteria_list.append(criteria)

        return CriteriaSet(criteria_list, spacing=spacing)

    def visit_criteria(self, node, criteria):
        criteria, = criteria
        return criteria

    def visit_single_criteria(self, node, single_criteria):
        criteria_name, = single_criteria
        return SingleCriteria(SingleCriteriaOption.from_string(criteria_name.text))

    def visit_parameterized_criteria(self, node, parameterized_criteria):
        criteria_option, _, parameter = parameterized_criteria
        return ParameterizedCriteria(ParameterizedCriteriaOption.from_string(criteria_option), parameter)

    def visit_exec_command(self, node, exec_command):
        _, space, command = exec_command
        return ExecCommand(command, spacing=[space])

    def visit_kill_command(self, node, kill_command):
        spacing = []
        target = KillTarget.NONE
        _, space_target = kill_command
        if type(space_target) == list:
            space_target, = space_target
            space, target = space_target
            spacing = [space]
            target, = target
            target = target.text
            target = KillTarget.from_string(target)

        return KillCommand(target, spacing=spacing)

    def visit_layout_toggle(self, node, layout_toggle):
        _, space, layout = layout_toggle
        layout, = layout
        layout._add_spacing_reversed(space)
        return layout

    def visit_layout_toggle_single(self, node, layout_toggle_single):
        split_or_all = layout_toggle_single
        split_or_all, = split_or_all
        return LayoutToggle(LayoutToggleOption.from_string(split_or_all), spacing=[])

    def visit_layout_toggle_multiple(self, node, layout_toggle_multiple):
        toggle_options = []
        spacing = []
        toggle0, space_toggles = layout_toggle_multiple
        toggle_options.append(toggle0)
        for space_toggle in space_toggles:
            space, toggle = space_toggle
            spacing.append(space)
            toggle_options.append(LayoutToggleBetweenOption.from_string(toggle))

        return LayoutToggleBetween(toggle_options, spacing=spacing)

    def visit_layout_command(self, node, layout_command):
        _, space, layout_command = layout_command
        layout_command, = layout_command
        if type(layout_command) == str:
            layout_mode = layout_command
            return LayoutSet(LayoutMode.from_string(layout_mode), spacing=[space])
        else:
            layout_command._add_spacing_reversed(space)
            return layout_command

    def visit_layout_multiple_option(self, node, layout_multiple_option):
        # This is always a list containing one string so
        # we just peel off the list layer
        return layout_multiple_option[0]

    def visit_mode_command(self, node, mode_command):
        _, space, mode_name = mode_command
        return ModeCommand(mode_name, spacing=[space])

    def visit_focus_command(self, node, focus_command):
        _, space, focus_instance_or_direction = focus_command
        focus_instance_or_direction, = focus_instance_or_direction

        if type(focus_instance_or_direction) == Direction:
            direction = focus_instance_or_direction
            return FocusDirection(direction, spacing=[space])
        else:
            focus_instance = focus_instance_or_direction
            focus_instance._add_spacing_reversed(space)
            return focus_instance

    def visit_focus_mode(self, node, focus_mode):
        focus_mode, = focus_mode
        focus_mode = focus_mode.text
        return FocusMode(FocusModeOption.from_string(focus_mode), spacing=[])

    def visit_focus_target(self, node, focus_target):
        focus_target, = focus_target
        focus_target = focus_target.text
        return FocusTarget(FocusTargetOption.from_string(focus_target), spacing=[])

    def visit_focus_output(self, node, focus_output):
        _, space, output_name = focus_output
        output_name = output_name
        return FocusOutput(output_name, spacing=[space])

    def visit_focus_relative(self, node, focus_relative):
        sibling_keyword = False
        spacing = []
        relative, space_sibling = focus_relative
        relative, = relative
        relative = relative.text
        if type(space_sibling) == list:
            space_sibling, = space_sibling
            space, sibling = space_sibling
            sibling_keyword = True
            spacing.append(space)

        return FocusRelative(FocusRelativeOption.from_string(relative), sibling_keyword, spacing=spacing)

    def visit_direction(self, node, direction):
        direction, = direction
        return Direction.from_string(direction.text)

    def visit_commands(self, node, commands):
        command, commands_and_other_stuff = commands
        commands = []
        spacing = []
        separators = []
        commands.append(command)
        # If there are more than one command
        if type(commands_and_other_stuff) == list:
            for space_separator_space_command in commands_and_other_stuff:
                space0_optional, separator, space1_optional, command = space_separator_space_command
                if type(space0_optional) == list:
                    space0, = space0_optional
                    spacing.append(space0)
                else:
                    # The CommandSet is one of the few cases in spacing where there's no
                    # good way to tell if spacing is required or not so we have to explicitly
                    # say that we want no spacing. In most other objects the number of spaces required
                    # can be inferred to some degree
                    spacing.append("")
                if type(separator) == list:
                    separator, = separator
                    separators.append(Separator.from_string(separator.text))
                if type(space1_optional) == list:
                    space1, = space1_optional
                    spacing.append(space1)
                else:
                    spacing.append("")
                commands.append(command)
        return CommandSet(commands, separators, spacing=spacing)

    def visit_command(self, node, command):
        command, = command
        return command

    def visit_move_command(self, node, move_command):
        # _: literal "move"
        # space_move_targets: list of lists with 2 elements each containing [space, <the move target>]
        # space1: some amount of space
        # move_tail: the move tail as returned by the relavent visit_move_xxxx method
        _, space_move_targets, space1, move_tail = move_command
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
        word = word
        spacing = [space]
        move_command = MoveToOutput(word, spacing=spacing)
        return move_command

    def visit_move_workspace_to(self, node, move_workspace_to) -> MoveWorkspaceTo:
        _, space0, _, space1, output_name = move_workspace_to
        output_name = output_name
        spacing = [space0, space1]
        move_command = MoveWorkspaceTo(output_name, spacing=spacing)
        return move_command

    def visit_move_to_mark(self, node, move_to_mark) -> MoveToMark:
        _, space, mark_name = move_to_mark
        mark_name = mark_name
        move_command = MoveToMark(mark_name)
        move_command._add_spacing_reversed(space)
        return move_command
    
    def visit_move_direction(self, node, move_direction):
        move_command = None
        direction, space_measurement = move_direction
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

    def visit_layout_default(self, node, layout_default):
        return node.text

    def visit_layout_all(self, node, layout_all):
        return node.text

    def visit_layout_split(self, node, layout_split):
        return node.text

    def visit_layout_mode(self, node, layout_mode):
        return node.text

    def visit_comment(self, node, comment):
        _, comment, _ = comment
        return CommentStatement(comment)

    def visit_empty_statement(self, node, empty_statement):
        return EmptyStatement()

    def visit_word_or_quoted_string(self, node, word_or_quoted_string):
        word_or_quoted_string, = word_or_quoted_string
        return word_or_quoted_string

    def visit_word(self, node, word):
        return node.text

    def visit_quoted_string(self, node, quoted_string):
        _, string_contents, _ = quoted_string
        return f'"{string_contents.text}"'

    def visit_variable(self, node, variable):
        _, variable_name = variable
        return Variable(variable_name)

    def visit_variable_name(self, node, variable_name):
        return node.text

    def visit_i3_word(self, node, i3_word):
        i3_word, = i3_word
        return i3_word

    def visit_symboless_word(self, node, symboless_word):
        return node.text

    def visit_rest(self, node, rest):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


if __name__ == "__main__":
    g = build_grammar()
    # This gets around a limitation where backslashes cannot be in f-strings
    newline = "\n"
    newline_replacement = "\\n"

    with open("diff.log", "w") as diff_file:
        for test_file in os.listdir("tests"):
            if os.path.exists("output.config"):
                os.remove("output.config")
            test_file = "tests/" + test_file
            print(f"Parsing {test_file}")
            with open(test_file, 'r') as config_file:
                config_text = config_file.read()
            ast = g.parse(config_text)
            I3ConfigVisitor().visit(ast)
            with open(test_file, 'r') as original:
                with open("output.config", 'r') as output:
                    for original_line, output_line in zip(original, output):
                        if original_line != output_line:
                            original_text = f"Original: '{original_line.replace(newline, newline_replacement)}'"
                            test_text     = f"Test:     '{output_line.replace(newline, newline_replacement)}'"
                            print(original_text)
                            print(test_text)
                            diff_file.write(original_text + "\n")
                            diff_file.write(test_text + "\n")

        