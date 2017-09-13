"""
Binary Ninja plugin for revealing stack character constants.
:author: Ben Cheney
:license: MIT
"""

from binaryninja.plugin import PluginCommand
from binaryninja.log import log_error
from binaryninja.interaction import get_form_input, AddressField
from binaryninja import enums

def reveal_stack_chars(view, start, length):
    """
    Takes a range of addresses from user input and sets the integer
    display type to ``enums.IntegerDisplayType.CharacterConstantDisplayType``
    for each instruction found. The address range must be within a
    single function.
    """

    start_addr_f = AddressField("Start address")
    end_addr_f = AddressField("End address")

    if not get_form_input(["Address range", start_addr_f, end_addr_f], "Reveal stack characters"):
        return

    funcs_1 = view.get_functions_containing(start_addr_f.result)
    funcs_2 = view.get_functions_containing(end_addr_f.result)

    if not funcs_1 or not funcs_2:
        log_error("Specified address range not contiguous within a single function.")
        return

    if funcs_1[0] != funcs_2[0]:
        log_error("Specified address range not contiguous within a single function.")
        return

    f = funcs_1[0]
    insts = [ inst for inst in f.low_level_il.basic_blocks[0]
                if inst.address >= start_addr_f.result and
                    inst.address <= end_addr_f.result ]
    for inst in insts:
          f.set_int_display_type(inst.address, value=inst.src.value.value, operand=1,
                                    display_type=enums.IntegerDisplayType.CharacterConstantDisplayType)

PluginCommand.register_for_range("Reveal stack characters", "Convert all selected integer args to character constants", reveal_stack_chars)
