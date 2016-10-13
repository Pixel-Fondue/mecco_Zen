#python

import lx, lxu, modo, kelvin, traceback

NAME = kelvin.symbols.ARGS_NAME
OPERATION = kelvin.symbols.ARGS_OPERATION
PRESET = kelvin.symbols.ARGS_PRESET

AUTO_OPERATION = kelvin.symbols.OPERATIONS_AUTO
ADD = kelvin.symbols.OPERATIONS_ADD
REMOVE = kelvin.symbols.OPERATIONS_REMOVE

NAME_CMD = kelvin.symbols.COMMAND_NAME_GROUP

class CMD_kelvin(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME, lx.symbol.sTYPE_STRING)
        self.dyna_Add(OPERATION, lx.symbol.sTYPE_STRING)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(1,3):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)


    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Execute(self, msg, flags):
        try:
            args = {}
            args[NAME] = self.dyna_String(0) if self.dyna_IsSet(0) else None
            args[OPERATION] = self.dyna_String(1) if self.dyna_IsSet(1) else AUTO_OPERATION
            args[PRESET] = self.dyna_String(2) if self.dyna_IsSet(2) else None

            selmode = kelvin.selection.get_mode()

            if args[OPERATION] in (AUTO_OPERATION,ADD):
                group = kelvin.items.group_selected_and_maskable(args[NAME])
                mask = kelvin.shadertree.build_material( group, preset = args[PRESET] )
                # kelvin.shadertree.cleanup()
                kelvin.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == REMOVE:
                items = kelvin.items.get_selected_and_maskable()
                groups = kelvin.items.get_groups(selected)
                kelvin.shadertree.seek_and_destroy(groups)
                # kelvin.shadertree.cleanup()

        except:
            traceback.print_exc()


lx.bless(CMD_kelvin, NAME_CMD)
