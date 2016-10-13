#python

import lx, lxu, modo, kelvin, traceback

NAME = kelvin.symbols.ARGS_NAME
MODE = kelvin.symbols.ARGS_MODE
OPERATION = kelvin.symbols.ARGS_OPERATION
CONNECTED = kelvin.symbols.ARGS_CONNECTED
PRESET = kelvin.symbols.ARGS_PRESET

AUTO_FILTER = kelvin.symbols.FILTER_TYPES_AUTO
MATERIAL = kelvin.symbols.FILTER_TYPES_MATERIAL
PART = kelvin.symbols.FILTER_TYPES_PART
PICK = kelvin.symbols.FILTER_TYPES_PICK
ITEM = kelvin.symbols.FILTER_TYPES_ITEM
ACTIVE = kelvin.symbols.FILTER_TYPES_ACTIVE
GLOC = kelvin.symbols.FILTER_TYPES_GLOC
GROUP = kelvin.symbols.FILTER_TYPES_GROUP

AUTO_OPERATION = kelvin.symbols.OPERATIONS_AUTO
OVERRIDE = kelvin.symbols.OPERATIONS_OVERRIDE
ADD = kelvin.symbols.OPERATIONS_ADD
REMOVE = kelvin.symbols.OPERATIONS_REMOVE

NAME_CMD = kelvin.symbols.COMMAND_NAME_BASE


class CMD_kelvin(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(NAME, lx.symbol.sTYPE_STRING)
        self.dyna_Add(MODE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(OPERATION, lx.symbol.sTYPE_STRING)
        self.dyna_Add(CONNECTED, lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(5):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)


    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO


    def basic_Execute(self, msg, flags):
        try:
            args = {}
            args[NAME] = self.dyna_String(0) if self.dyna_IsSet(0) else None
            args[MODE] = self.dyna_String(1) if self.dyna_IsSet(1) else AUTO_FILTER
            args[OPERATION] = self.dyna_String(2) if self.dyna_IsSet(2) else None
            args[CONNECTED] = self.dyna_Bool(3) if self.dyna_IsSet(3) else None
            args[PRESET] = self.dyna_String(4) if self.dyna_IsSet(4) else None

            selmode = kelvin.selection.get_mode()

            if args[MODE] == AUTO_FILTER:
                if selmode in ['polygon','ptag']:
                    args[MODE] = MATERIAL
                    if args[OPERATION] == REMOVE:
                        args[NAME] = REMOVE

                elif selmode in ['edge','vertex']:
                    args[MODE] = MATERIAL
                    args[CONNECTED] = True
                elif selmode == ITEM:
                    if len(kelvin.items.get_selected_and_maskable()) == 0:
                        args[MODE] = ACTIVE
                    elif len(kelvin.items.get_selected_and_maskable()) == 1:
                        args[MODE] = ITEM
                    else:
                        args[MODE] = GROUP
                else:
                    return False


            if args[MODE] in (MATERIAL,PART,PICK):
                if args[OPERATION] == REMOVE:
                    args[NAME] = REMOVE
                lx.eval(kelvin.symbols.COMMAND_NAME_PTAG + kelvin.util.build_arg_string(args))

            elif args[MODE] in (ITEM,ACTIVE):
                del args[NAME]
                del args[CONNECTED]
                lx.eval(kelvin.symbols.COMMAND_NAME_ITEM + kelvin.util.build_arg_string(args))

            elif args[MODE] == GROUP:
                del args[MODE]
                del args[CONNECTED]
                lx.eval(kelvin.symbols.COMMAND_NAME_GROUP + kelvin.util.build_arg_string(args))


        except:
            traceback.print_exc()


lx.bless(CMD_kelvin, NAME_CMD)
