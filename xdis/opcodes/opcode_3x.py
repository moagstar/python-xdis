"""
CPython 3.2 bytecode opcodes to be used as a base for other opcodes including 3.2.

This is used in bytecode disassembly among other things. This is
similar to the opcodes in Python's opcode.py library.

If this file changes the other opcode files may have to a adjusted accordingly.
"""

from xdis.opcodes.base import (
    compare_op, const_op,
    def_op, format_extended_arg,
    free_op, jabs_op, jrel_op,
    local_op, name_op, nargs_op,
    varargs_op
    )

l = locals()

# FIXME: DRY with opcode2x.py

hasconst = []
hasname = []
hasjrel = []
hasjabs = []
haslocal = []
hascompare = []
hasfree = []
hasnargs = []  # For function-like calls
hasvargs = []  # Similar but for operators BUILD_xxx

# opmap[opcode_name] => opcode_number
opmap = {}

# opcode[i] => opcode name
opname = [''] * 256

# oppush[op] => number of stack entries pushed
oppush = [0] * 256

# oppop[op] => number of stack entries popped
oppop  = [0] * 256

for op in range(256): opname[op] = '<%r>' % (op,)
del op

# Instruction opcodes for compiled code
# Blank lines correspond to available opcodes

#          OP NAME            OPCODE POP PUSH
#--------------------------------------------
def_op(l, 'STOP_CODE',             0,  0,  0)
def_op(l, 'POP_TOP',               1,  1,  0)
def_op(l, 'ROT_TWO',               2,  2,  2)
def_op(l, 'ROT_THREE',             3,  3,  3)
def_op(l, 'DUP_TOP',               4,  0,  1)

# Python 3.2+
def_op(l, 'DUP_TOP_TWO',           5,  0,  2)

def_op(l, 'NOP', 9)
def_op(l, 'UNARY_POSITIVE',       10,  1,  1)
def_op(l, 'UNARY_NEGATIVE',       11,  1,  1)
def_op(l, 'UNARY_NOT',            12,  1,  1)

def_op(l, 'UNARY_INVERT',         15,  1,  1)

def_op(l, 'BINARY_POWER',         19,  2,  1)
def_op(l, 'BINARY_MULTIPLY',      20,  2,  1)

def_op(l, 'BINARY_MODULO',        22,  2,  1)
def_op(l, 'BINARY_ADD',           23,  2,  1)
def_op(l, 'BINARY_SUBTRACT',      24,  2,  1)
def_op(l, 'BINARY_SUBSCR',        25,  2,  1)
def_op(l, 'BINARY_FLOOR_DIVIDE',  26,  2,  1)
def_op(l, 'BINARY_TRUE_DIVIDE',   27,  2,  1)
def_op(l, 'INPLACE_FLOOR_DIVIDE', 28,  2,  1)
def_op(l, 'INPLACE_TRUE_DIVIDE',  29,  2,  1)

# Gone from Python 3 are Python2's
# SLICE+0 .. SLICE+3
# STORE_SLICE+0 .. STORE_SLICE+3
# DELETE_SLICE+0 .. DELETE_SLICE+3

def_op(l, 'STORE_MAP', 54)
def_op(l, 'INPLACE_ADD',          55,  2,  1)
def_op(l, 'INPLACE_SUBTRACT',     56,  2,  1)
def_op(l, 'INPLACE_MULTIPLY',     57,  2,  1)

def_op(l, 'INPLACE_MODULO',       59,  2,  1)
def_op(l, 'STORE_SUBSCR',         60,  2,  1)
def_op(l, 'DELETE_SUBSCR',        61,  2,  0)
def_op(l, 'BINARY_LSHIFT',        62,  2,  1)
def_op(l, 'BINARY_RSHIFT',        63,  2,  1)
def_op(l, 'BINARY_AND',           64,  2,  1)
def_op(l, 'BINARY_XOR',           65,  2,  1)
def_op(l, 'BINARY_OR',            66,  2,  1)
def_op(l, 'INPLACE_POWER',        67,  2,  1)
def_op(l, 'GET_ITER',             68,  1,  1)
def_op(l, 'STORE_LOCALS', 69)

def_op(l, 'PRINT_EXPR',           70,  1,  0)
def_op(l, 'LOAD_BUILD_CLASS',     71,  0,  1)

# Python3 drops/changes:
#  def_op(l, 'PRINT_ITEM', 71)
#  def_op(l, 'PRINT_NEWLINE', 72)
#  def_op(l, 'PRINT_ITEM_TO', 73)
#  def_op(l, 'PRINT_NEWLINE_TO', 74)

def_op(l, 'INPLACE_LSHIFT',       75,  2,  1)
def_op(l, 'INPLACE_RSHIFT',       76,  2,  1)
def_op(l, 'INPLACE_AND',          77,  2,  1)
def_op(l, 'INPLACE_XOR',          78,  2,  1)
def_op(l, 'INPLACE_OR',           79,  2,  1)
def_op(l, 'BREAK_LOOP',           80,  0,  0)
def_op(l, 'WITH_CLEANUP', 81)

def_op(l, 'RETURN_VALUE',         83,  1,  0)
def_op(l, 'IMPORT_STAR',          84,  1,  0)

def_op(l, 'YIELD_VALUE',          86,  1,  1)
def_op(l, 'POP_BLOCK',            87,  0,  0)
def_op(l, 'END_FINALLY',          88,  1,  0)
def_op(l, 'POP_EXCEPT',           89,  1, -1)

HAVE_ARGUMENT = 90              # Opcodes from here have an argument:

name_op(l, 'STORE_NAME',            90,  1,  0)   # Operand is in name list
name_op(l, 'DELETE_NAME',           91,  0,  0)   # ""
varargs_op(l, 'UNPACK_SEQUENCE',    92, -1,  1)   # Number of tuple items
jrel_op(l,    'FOR_ITER',           93, -1, -1)

def_op(l,  'UNPACK_EX', 94)
name_op(l, 'STORE_ATTR',            95,  2,  0)   # Operand is in name list
name_op(l, 'DELETE_ATTR',           96,  1,  0)   # ""
name_op(l, 'STORE_GLOBAL',          97,  1,  0)   # ""
name_op(l, 'DELETE_GLOBAL',         98,  0,  0)   # ""

# Python 2's DUP_TOPX is gone starting in Python 3.2

const_op(l,   'LOAD_CONST',        100,  0,  1)  # Operand is in const list
name_op(l,    'LOAD_NAME',         101,  0,  1)  # Operand is in name list
varargs_op(l, 'BUILD_TUPLE',       102, -1,  1)  # TOS is count of tuple items
varargs_op(l, 'BUILD_LIST',        103, -1,  1)  # TOS is count of list items
varargs_op(l, 'BUILD_SET',         104, -1,  1)  # TOS is count of set items
varargs_op(l, 'BUILD_MAP',         105, -1,  1)  # TOS is count of kwarg items
name_op(l, 'LOAD_ATTR',            106,  1,  1)  # Operand is in name list
compare_op(l, 'COMPARE_OP',        107,  2,  1)  # Comparison operator
name_op(l, 'IMPORT_NAME',          108,  1,  1)  # Operand is in name list
name_op(l, 'IMPORT_FROM',          109,  0,  1)  # Operand is in name list

jrel_op(l, 'JUMP_FORWARD',         110,  0,  0)  # Number of bytes to skip
jabs_op(l, 'JUMP_IF_FALSE_OR_POP', 111)          # Target byte offset from beginning of code
jabs_op(l, 'JUMP_IF_TRUE_OR_POP',  112)          # ""
jabs_op(l, 'JUMP_ABSOLUTE',        113,  0,  0)  # Target byte offset from beginning of code
jabs_op(l, 'POP_JUMP_IF_FALSE',    114)          # ""
jabs_op(l, 'POP_JUMP_IF_TRUE',     115)          # ""

name_op(l, 'LOAD_GLOBAL',          116,  0,  1)  # Operand is in name list

jabs_op(l, 'CONTINUE_LOOP',        119,  0,  0)  # Target address
jrel_op(l, 'SETUP_LOOP',           120,  0,  0)  # Distance to target address
jrel_op(l, 'SETUP_EXCEPT',         121,  0,  0)  # ""
jrel_op(l, 'SETUP_FINALLY',        122,  0,  0)  # ""

local_op(l, 'LOAD_FAST',           124,  0,  1)  # Local variable number
local_op(l, 'STORE_FAST',          125,  1,  0)  # Local variable number
local_op(l, 'DELETE_FAST',         126,  0,  0)  # Local variable number

def_op(l, 'RAISE_VARARGS',         130, -1,  0)  # Number of raise arguments (1, 2, or 3)
nargs_op(l, 'CALL_FUNCTION',       131, -1,  1)  # #args + (#kwargs << 8)

def_op(l, 'MAKE_FUNCTION',         132, -1,  1)  # Number of args if < 3.6
varargs_op(l, 'BUILD_SLICE',       133, -1,  1)  # Number of items

def_op(l, 'MAKE_CLOSURE',          134, -1,  1)
free_op(l, 'LOAD_CLOSURE',         135,  0,  1)
free_op(l, 'LOAD_DEREF',           136,  0,  1)
free_op(l, 'STORE_DEREF',          137,  1,  0)
free_op(l, 'DELETE_DEREF',         138,  0,  0)

nargs_op(l, 'CALL_FUNCTION_VAR',   140, -1,  1)  # #args + (#kwargs << 8)
nargs_op(l, 'CALL_FUNCTION_KW',    141, -1,  1)  # #args + (#kwargs << 8)
nargs_op(l, 'CALL_FUNCTION_VAR_KW',142, -1, 1)   # #args + (#kwargs << 8)

jrel_op(l, 'SETUP_WITH',           143,  0,  7)

def_op(l, 'LIST_APPEND',           145,  2,  1)  # Calls list.append(TOS[-i], TOS).
                                                 # Used to implement list comprehensions.
def_op(l, 'SET_ADD',               146,  1,  0)
def_op(l, 'MAP_ADD',               147,  2,  1)

def_op(l, 'EXTENDED_ARG', 144)
EXTENDED_ARG = 144

def format_MAKE_FUNCTION_arg(argc):
    pos_args = argc & 0xFF
    name_default = (argc >> 8) & 0xFF
    annotate_args = (argc >> 16) & 0x7FFF
    return ("%d positional, %d name and default, %d annotations" %
            (pos_args, name_default, annotate_args))

opcode_arg_fmt = {
    'EXTENDED_ARG': format_extended_arg
}
