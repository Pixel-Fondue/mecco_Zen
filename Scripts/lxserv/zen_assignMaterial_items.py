#python

import lx, lxu, modo, zen, traceback

MODE = zen.symbols.ARGS_MODE
OPERATION = zen.symbols.ARGS_OPERATION
PRESET = zen.symbols.ARGS_PRESET

AUTO_FILTER = zen.symbols.FILTER_TYPES_AUTO
ITEM = zen.symbols.FILTER_TYPES_ITEM
ACTIVE = zen.symbols.FILTER_TYPES_ACTIVE
GLOC = zen.symbols.FILTER_TYPES_GLOC
GROUP = zen.symbols.FILTER_TYPES_GROUP

AUTO_OPERATION = zen.symbols.OPERATIONS_AUTO
ADD = zen.symbols.OPERATIONS_ADD
REMOVE = zen.symbols.OPERATIONS_REMOVE

NAME_CMD = zen.symbols.COMMAND_NAME_ITEM

class CMD_zen(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(MODE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(OPERATION, lx.symbol.sTYPE_STRING)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(3):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)


    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Execute(self, msg, flags):
        try:
            args = {}
            args[MODE] = self.dyna_String(0) if self.dyna_IsSet(0) else AUTO_FILTER
            args[OPERATION] = self.dyna_String(1) if self.dyna_IsSet(1) else AUTO_OPERATION
            args[PRESET] = self.dyna_String(2) if self.dyna_IsSet(2) else None

            selmode = zen.selection.get_mode()

            items = (
                zen.items.get_active_layers() if args[MODE] == ACTIVE
                else zen.items.get_selected_and_maskable()
            )

            if args[OPERATION] == AUTO_OPERATION:
                for item in items:
                    if zen.shadertree.get_masks(item):
                        zen.shadertree.seek_and_destroy(item)
                    mask = zen.shadertree.build_material( item, preset = args[PRESET] )
                    zen.shadertree.cleanup()
                    zen.shadertree.move_to_top(mask)

            if args[OPERATION] == ADD:
                for item in items:
                    mask = zen.shadertree.build_material( item, preset = args[PRESET] )
                    zen.shadertree.cleanup()
                    zen.shadertree.move_to_top(mask)

            if args[OPERATION] == REMOVE:
                items = modo.Scene().selected
                zen.shadertree.seek_and_destroy(items)
                zen.shadertree.cleanup()


        except:
            traceback.print_exc()


lx.bless(CMD_zen, NAME_CMD)
