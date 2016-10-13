#python

import lx

COMMAND_NAME_BASE = 'kelvin.setMaterial'
COMMAND_NAME_PTAG = 'kelvin.setMaterial_pTag'
COMMAND_NAME_ITEM = 'kelvin.setMaterial_item'
COMMAND_NAME_GROUP = 'kelvin.setMaterial_group'

GROUPNAME = "group"
MATNAME = "material"
SHADERNAME = "shader"
BASE_SHADER = 'Base Shader'
BASE_MATERIAL = 'Base Material'

GTYP = "GTYP"

GROUP_TYPES_STANDARD = ''
GROUP_TYPES_ASSEMBLY = 'assembly'

ARGS_NAME = 'name'
ARGS_MODE = 'mode'
ARGS_OPERATION = 'operation'
ARGS_CONNECTED = 'connected'
ARGS_PRESET = 'preset'
ARGS_COPY = 'copy'
ARGS_PASTE = 'paste'

FILTER_TYPES_AUTO = 'auto'
FILTER_TYPES_MATERIAL = 'material'
FILTER_TYPES_PART = 'part'
FILTER_TYPES_PICK = 'selection'
FILTER_TYPES_ITEM = 'item'
FILTER_TYPES_ACTIVE = 'active'
FILTER_TYPES_GLOC = 'folder'
FILTER_TYPES_GROUP = 'group'

OPERATIONS_AUTO = 'auto'
OPERATIONS_OVERRIDE = 'override'
OPERATIONS_ADD = 'add'
OPERATIONS_REMOVE = 'remove'

def sICHAN_MASK_PTYP(i_POLYTAG):
    """Returns a suitable string for a mask item's lx.symbol.sICHAN_MASK_PTYP channel
    based on an lx.symbol.i_POLYTAG_* symbol."""

    return {
        lx.symbol.i_POLYTAG_MATERIAL:'Material',
        lx.symbol.i_POLYTAG_PICK:'Selection Set',
        lx.symbol.i_POLYTAG_PART:'Part'
    }[i_POLYTAG]

def i_POLYTAG(sICHAN_MASK_PTYP):
    """Returns an lx.symbol.i_POLYTAG_* symbol based on a mask
    item's lx.symbol.sICHAN_MASK_PTYP channel string."""

    return {
        '':lx.symbol.i_POLYTAG_MATERIAL,
        'Material':lx.symbol.i_POLYTAG_MATERIAL,
        'Selection Set':lx.symbol.i_POLYTAG_PICK,
        'Part':lx.symbol.i_POLYTAG_PART
    }[sICHAN_MASK_PTYP]
