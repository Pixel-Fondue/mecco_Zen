#python

import lx, lxu, modo, zen, traceback

NAME = zen.symbols.ARGS_NAME
OPERATION = zen.symbols.ARGS_OPERATION
PRESET = zen.symbols.ARGS_PRESET

AUTO_OPERATION = zen.symbols.OPERATIONS_AUTO
ADD = zen.symbols.OPERATIONS_ADD
REMOVE = zen.symbols.OPERATIONS_REMOVE

NAME_CMD = zen.symbols.COMMAND_NAME_GROUP

class CMD_zen(lxu.command.BasicCommand):

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

            selmode = zen.selection.get_mode()

            if args[OPERATION] in (AUTO_OPERATION,ADD):
                group = zen.items.group_selected_and_maskable(args[NAME])
                mask = zen.shadertree.build_material( group, preset = args[PRESET] )
                # zen.shadertree.cleanup()
                zen.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == REMOVE:
                items = zen.items.get_selected_and_maskable()
                groups = zen.items.get_groups(selected)
                zen.shadertree.seek_and_destroy(groups)
                # zen.shadertree.cleanup()

        except:
            traceback.print_exc()


lx.bless(CMD_zen, NAME_CMD)
