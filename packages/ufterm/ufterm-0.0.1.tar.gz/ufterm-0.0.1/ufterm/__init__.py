import sys
import readline
import os
import textwrap

from os import path
from enum import Enum
from datetime import datetime
from typing import Union, Tuple, Callable, TypeVar, Type, Generic

from .register import Register
from .exception import *
from .utils import convert_str_to_type, is_empty_str, get_digit_number


# Save the standard print and input into a private variable to avoid error in case the developer alias them
_std_print, _std_input = print, input

########################################################################################################################
# Type Definition

ValueType = TypeVar('ValueType', str, int, float, bool)
InputDef = Union[Tuple[str, Type[ValueType]],
                 Tuple[str, Type[ValueType], ValueType],
                 Tuple[str, Type[ValueType], ValueType, Callable[[ValueType], bool]]]
FormInputDefTuple = InputDef[Union[str, int, float, bool]]
########################################################################################################################


class MsgType(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3


# Reassign the enum variable to for more convenient naming
INFO_MSG = MsgType.INFO
WARNING_MSG = MsgType.WARNING
ERROR_MSG = MsgType.ERROR


# A simple class where store the private module variable
class _PrivateVar:
    gui = None
    done = False
    commands = {}
    selected_command = None


def print_(text: str, msg_type: MsgType = MsgType.INFO):
    """
    Display a message to the user.
    The warning and error message are display on the error output with the terminal mode.

    :param      text:  Message to display
    :param  msg_type:  Type of message. The warning will be orange and error red.
    """
    text = textwrap.indent(text, '           ')
    text = text.replace('          ', datetime.now().strftime('[%H:%M:%S]'), 1)
    if _PrivateVar.gui is not None:
        _PrivateVar.gui.insert_text(text, msg_type.name)
    else:
        if msg_type != INFO_MSG:
            _std_print(text, file=sys.stderr)
        else:
            _std_print(text)


def _get_default_default_value(type_: Type[ValueType]) -> ValueType:
    if type_ is int:
        return 0
    elif type_ is float:
        return 0.
    elif type_ is bool:
        return False
    elif type_ is str:
        return ""
    raise TypeError("Unsupported type")


def input_(label: str = "",
           history_id: str = None,
           type_: Type[ValueType] = str,
           default_value: ValueType = None,
           validator: Callable[[ValueType], bool] = lambda s: True) -> ValueType:
    """
    Ask users to enter some data. Then convert and check the value before returning it.

    :param          label:  The prompt (text displayed right before the area where the user is going write).
    :param     history_id:  Optional id to record values entered to create a history.
    :param          type_:  The type of the value that have to be converted to.
    :param  default_value:  Optional pre-set value inside the area where the user enter the data
                            (This only work on Linux terminal and GUI interface)
    :param      validator:  Function that will validate the data entered

    :return: The value entered by the user checked and converted to the right type.
    """
    if default_value is None:
        default_value = _get_default_default_value(type_)
    if _PrivateVar.gui is not None:
        return _PrivateVar.gui.get_user_input(label, type_, default_value, history_id, validator)
    else:
        readline.set_completer(None)
        return _terminal_input(label, type_, default_value, history_id, validator)


def get_file_path(label: str = "Please select the file path: ",
                  history_id: str = None,
                  default_value: str = "",
                  have_to_exist: bool = False):
    """
    Ask users to select a file path. The function can check if the file exist before returning.

    :param          label:  The prompt (text displayed right before the area where the user is going write).
    :param     history_id:  Optional id to record values entered to create a history.
    :param  default_value:  Optional pre-set value inside the area where the user enter the data
                            (This only work on Linux terminal and GUI interface)
    :param  have_to_exist:  Define if the file have to exist or not.

    :return:  The file path as a string.
    """
    def my_completer(text: str, state: int):
        """
        auto-complete override function for the readline library.
        """
        # We replace the slash by the correct path separator depending on the platform.
        text = text.replace("/", path.sep)
        competing_folder, completing_file = path.split(text)
        working_path = path.join(os.getcwd(), competing_folder)
        try:
            results = [f for f in os.listdir(working_path) if f.startswith(completing_file) and not f.startswith(".")]
        except FileNotFoundError:
            results = []

        # If they are only 1 solution and the text completed is a folder ...
        if len(results) == 1 and path.isdir(path.join(os.getcwd(), completing_file)):
            # ... we add the path separator at the end.
            results = [path.join(competing_folder, completing_file, '')]
        else:
            # ... otherwise we re-merge the completing_folder part.
            results = [path.join(competing_folder, f) for f in results]
            # For each propositions ...
            for i, tmp in enumerate(results):
                if path.isdir(path.join(os.getcwd(), tmp)):
                    # ... we add a the path separator to the one which are folder.
                    results[i] = path.join(tmp, '')

        # The library require a list ending by None.
        # results.append(None)  # The code work even without
        return results[state]

    if _PrivateVar.gui is not None:
        return _PrivateVar.gui.get_user_input(label, str, history_id)
    else:
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims('\n')
        readline.set_completer(my_completer)
        result = _terminal_input(label, str, default_value, history_id)
        if have_to_exist:
            if not path.isfile(result):
                _std_print("The file '%s' doesn't exist" % result, file=sys.stderr)
                return get_file_path(label, history_id, result, have_to_exist)
        return result


def _terminal_input(label: str,
                    type_: Type[ValueType],
                    default_value: ValueType,
                    id_: str = None,
                    validator: Callable[[ValueType], bool] = lambda v: True) -> ValueType:

    readline.clear_history()
    readline.set_startup_hook(lambda: readline.insert_text(str(default_value)))
    while True:
        _std_print("\r", end="")
        sys.stdout.flush()
        sys.stderr.flush()
        last_value = ""
        if id_ is not None:
            for previous_value in Register.get("input_history", {}).get(id_, []):
                readline.add_history(previous_value)
                last_value = previous_value
        result = _std_input(label)
        if id_ is not None and result != last_value and not is_empty_str(result):
            Register["input_history"][id_].append(result)
        try:
            res = convert_str_to_type(result, type_)
            if validator(res):
                return res
            else:
                _std_print("The value n'est pas correct", file=sys.stderr)
        except ConversionError as error:
            _std_print(error, file=sys.stderr)


def _enumerate_input_def(form_definition, form_id):
    def generate_input_label(pos):
        return "%s_input_%0*d" % (form_id, number_of_zero, pos)

    number_of_zero = get_digit_number(len(form_definition))

    for i, input_definition in enumerate(form_definition):
        default = input_definition[2] if len(input_definition) >= 3 else None
        validator = input_definition[3] if len(input_definition) == 4 else lambda s: True
        yield input_definition[0], generate_input_label(i + 1), input_definition[1], default, validator


def form(form_definition: Tuple[FormInputDefTuple, ...], form_history_id: str = None) -> Tuple[ValueType, ...]:
    """
    Ask users to enter multiple values.

    :param  form_definition:  See the input_ parameter definition.
                              The only parameter to omit is the history_id.
    :param  form_history_id:  Optional id to record values entered to create a history.

    :return:
    """
    result = []
    for label, input_id, type_, default, validator in _enumerate_input_def(form_definition, form_history_id):
        result.append(input_(label, input_id, type_, default, validator))

    return tuple(result)


def done():
    """
    Set the program as done. That mean it is going to stop at the next loop
    """

    _PrivateVar.done = True


def is_done():
    """
    :return:  The value to know if the current program is finish or not
    """
    return _PrivateVar.done


def reset():
    """
    Reset the module to its original state
    """
    _PrivateVar.gui = None
    _PrivateVar.done = False
    _PrivateVar.commands = {}
    _PrivateVar.selected_command = None


def add_command(command: callable, custom_name: str = None):
    """
    Add a command to the module.

    :param      command:  Command to be add to the choice
    :param  custom_name:
    """
    if command in _PrivateVar.commands.values():
        raise CommandAlreadyPresentError(command.__name__)
    if custom_name is None:
        custom_name = command.__name__
    if custom_name in _PrivateVar.commands:
        raise CommandNameAlreadyUsedError(custom_name)
    _PrivateVar.commands[custom_name] = command


def run_command():
    if len(_PrivateVar.commands) == 1:
        _PrivateVar.selected_command = _PrivateVar.commands[list(_PrivateVar.commands.keys())[0]]
    if _PrivateVar.selected_command is None:
        raise NoCommandSelectedError()
    _PrivateVar.selected_command()


def loop():
    def looping():
        while not is_done():
            if _PrivateVar.selected_command is None:
                _display_menu()
            else:
                _PrivateVar.selected_command()
                _PrivateVar.selected_command = None

    if _PrivateVar.gui is None:
        looping()


def _display_menu():
    if _PrivateVar.gui is None:
        for i, (name, command) in enumerate(_PrivateVar.commands.items()):
            _std_print("[%3d]: %s" % (i, name))

        done_ = False
        while not done_:
            try:
                result = input("Select the command: ")
                result = result.upper()
                if result == "EXIT" or result == "CANCEL" or result == "QUIT":
                    done()
                    break
                result = int(result)
                if 0 <= result < len(_PrivateVar.commands):
                    keys = _PrivateVar.commands.keys()
                    _PrivateVar.selected_command = _PrivateVar.commands[list(_PrivateVar.commands.keys())[result]]
                    done_ = True
                else:
                    _std_print("This command is not define. Please select one in the range [0-%d]" %
                               (len(_PrivateVar.commands) - 1))
            except EOFError:
                done()
                break
            except ValueError:
                _std_print("Use exit/quit/cancel or Ctrl-D to exit")
