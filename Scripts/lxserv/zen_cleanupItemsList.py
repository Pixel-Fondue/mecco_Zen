#python

import lx, lxu, modo, zen, traceback

NAME_CMD = 'zen.cleanupItemsList'

class CMD_zen(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Execute(self, msg, flags):
        try:
            zen.items.cleanup()

        except:
            traceback.print_exc()


lx.bless(CMD_zen, NAME_CMD)
