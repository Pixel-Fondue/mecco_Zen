# python

import lx, lxifc, lxu.command

class CommandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('cmd', lx.symbol.sTYPE_STRING)
        self.dyna_Add('label', lx.symbol.sTYPE_STRING)
        self.dyna_Add('recommended', lx.symbol.sTYPE_STRING)

    def basic_ButtonName(self):
        return "%s \x03(c:25132927)(Recommended: %s)" % (self.dyna_String(1), self.dyna_String(2))

    def cmd_Execute(self,flags):
        lx.eval("%s" % self.dyna_String(0))

lx.bless(CommandClass, "zen.labeledPopover")

class CommandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('cmd', lx.symbol.sTYPE_STRING)
        self.dyna_Add('label', lx.symbol.sTYPE_STRING)

    def basic_ButtonName(self):
        return 'Map "%s" to key...' % self.dyna_String(1)

    def cmd_Execute(self,flags):
        lx.eval('cmds.mapKey {} "%s" .global (stateless) .anywhere' % self.dyna_String(0))

lx.bless(CommandClass, "zen.labeledMapKey")
