# python

import lx, lxifc, lxu
from zen import CommanderClass

CMD_NAME = 'zen.framesPie'

class CommandClass(CommanderClass):

    def commander_execute(self, msg, flags):

        if lx.eval("user.value right_handed_lists ?"):
            lx.eval('attr.formPopover {ZenPie_Frames_R:sheet}')
        else:
            lx.eval('attr.formPopover {ZenPie_Frames_L:sheet}')


lx.bless(CommandClass, CMD_NAME)
