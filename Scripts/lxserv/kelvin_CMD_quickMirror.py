#!/usr/bin/env python

import lx
import lxifc
import lxu
import lxu.command
import traceback

class kelvin_QuickMirror(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        # ARGUMENTS DEFINED HERE:
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('axis', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('tolerance', lx.symbol.sTYPE_DISTANCE)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())
            lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

    def CMD_EXE(self, msg, flags):

        # GRAB ARGUMENTS HERE:
        axis = self.dyna_String(0, 0.0)
        if (axis == 'x'):
            axis = 0
        elif axis == 'y':
            axis = 1
        elif axis == 'z':
            axis = 2
        else:
            axis = 0

        tolerance = self.dyna_String(1, 0.0)
        if tolerance == '':
            tolerance = '0'

        # CODE GOES HERE:
        lx.eval('tool.set *.mirror on')
        lx.eval('tool.attr gen.mirror axis %s' % axis)
        lx.eval('tool.attr gen.mirror cenX 0.0')
        lx.eval('tool.attr gen.mirror cenY 0.0')
        lx.eval('tool.attr gen.mirror cenZ 0.0')
        lx.eval('tool.attr gen.mirror upX 0.0')
        lx.eval('tool.attr gen.mirror upY 0.0')
        lx.eval('tool.attr gen.mirror upZ 0.0')
        lx.eval('tool.attr effector.clone replace false')
        lx.eval('tool.attr effector.clone dist %s' % tolerance)
        lx.eval('tool.doApply')
        lx.eval('tool.drop')

    def basic_Enable(self,msg):
        return True

lx.bless(kelvin_QuickMirror, "kelvin.quickMirror")
