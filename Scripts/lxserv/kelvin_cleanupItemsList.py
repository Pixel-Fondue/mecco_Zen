#python

import lx, lxu, modo, kelvin, traceback

NAME_CMD = 'kelvin.cleanupItemsList'

class CMD_kelvin(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Execute(self, msg, flags):
        try:
            kelvin.items.cleanup()

        except:
            traceback.print_exc()


lx.bless(CMD_kelvin, NAME_CMD)
