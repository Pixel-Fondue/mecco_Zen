#python

import lx, lxu, modo, kelvin, traceback

MODE = kelvin.symbols.ARGS_MODE
OPERATION = kelvin.symbols.ARGS_OPERATION
PRESET = kelvin.symbols.ARGS_PRESET

AUTO_FILTER = kelvin.symbols.FILTER_TYPES_AUTO
ITEM = kelvin.symbols.FILTER_TYPES_ITEM
ACTIVE = kelvin.symbols.FILTER_TYPES_ACTIVE
GLOC = kelvin.symbols.FILTER_TYPES_GLOC
GROUP = kelvin.symbols.FILTER_TYPES_GROUP

AUTO_OPERATION = kelvin.symbols.OPERATIONS_AUTO
ADD = kelvin.symbols.OPERATIONS_ADD
REMOVE = kelvin.symbols.OPERATIONS_REMOVE

NAME_CMD = kelvin.symbols.COMMAND_NAME_ITEM

class CMD_kelvin(lxu.command.BasicCommand):

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

            selmode = kelvin.selection.get_mode()

            items = (
                kelvin.items.get_active_layers() if args[MODE] == ACTIVE
                else kelvin.items.get_selected_and_maskable()
            )

            if args[OPERATION] == AUTO_OPERATION:
                for item in items:
                    if kelvin.shadertree.get_masks(item):
                        kelvin.shadertree.seek_and_destroy(item)
                    mask = kelvin.shadertree.build_material( item, preset = args[PRESET] )
                    # kelvin.shadertree.cleanup()
                    kelvin.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == ADD:
                for item in items:
                    mask = kelvin.shadertree.build_material( item, preset = args[PRESET] )
                    # kelvin.shadertree.cleanup()
                    kelvin.shadertree.move_to_base_shader(mask)

            if args[OPERATION] == REMOVE:
                items = modo.Scene().selected
                kelvin.shadertree.seek_and_destroy(items)
                # kelvin.shadertree.cleanup()


        except:
            traceback.print_exc()


lx.bless(CMD_kelvin, NAME_CMD)
