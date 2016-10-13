#python

import lx, lxu, modo, kelvin, traceback

NAME_CMD = 'kelvin.pTagClipboard'

COPY = kelvin.symbols.ARGS_COPY
PASTE = kelvin.symbols.ARGS_PASTE

MATERIAL = kelvin.symbols.FILTER_TYPES_MATERIAL

NAME = kelvin.symbols.ARGS_NAME
MODE = kelvin.symbols.ARGS_MODE
CONNECTED = kelvin.symbols.ARGS_CONNECTED
PRESET = kelvin.symbols.ARGS_PRESET

class CMD_kelvin(lxu.command.BasicCommand):

    _clipboard = ''

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add(MODE, lx.symbol.sTYPE_STRING)
        self.dyna_Add(CONNECTED, lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add(PRESET, lx.symbol.sTYPE_STRING)

        for i in range(3):
            self.basic_SetFlags(i, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    @classmethod
    def set_clipboard(cls, value):
        cls._clipboard = value

    def basic_Execute(self, msg, flags):
        try:
            mode = self.dyna_String(0) if self.dyna_IsSet(0) else COPY

            if mode == COPY:
                self.set_clipboard(kelvin.selection.get_polys()[0].tags()['material'])

            elif mode == PASTE:
                args = {}
                args[NAME] = self._clipboard
                args[MODE] = MATERIAL
                args[CONNECTED] = self.dyna_Bool(1) if self.dyna_IsSet(1) else None

                lx.eval(kelvin.symbols.COMMAND_NAME_PTAG + kelvin.util.build_arg_string(args))

        except:
            traceback.print_exc()


lx.bless(CMD_kelvin, NAME_CMD)
