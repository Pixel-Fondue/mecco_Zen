#!/usr/bin/env python

import lx
import lxifc
import lxu
import lxu.command
import traceback

class kelvin_quickRadial(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        # ARGUMENTS DEFINED HERE:
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('axis', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('sides', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('tolerance', lx.symbol.sTYPE_DISTANCE)
        self.basic_SetFlags(3, lx.symbol.fCMDARG_OPTIONAL)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())
            lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

    def CMD_EXE(self, msg, flags):

        try:
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

            sides = self.dyna_String(2, 0.0)
            if sides == '':
                sides = '5'

            tolerance = self.dyna_String(2, 0.0)
            if tolerance == '':
                tolerance = '0'

            # CODE GOES HERE:
            lx.eval('tool.set "*.Radial Array" on')
            lx.eval('tool.attr gen.helix axis %s' % axis)
            lx.eval('tool.attr gen.helix sides %s' % sides)
            lx.eval('tool.attr gen.helix vecX 0.0')
            lx.eval('tool.attr gen.helix vecY 0.0')
            lx.eval('tool.attr gen.helix vecZ 0.0')
            lx.eval('tool.attr gen.helix end 360.0')
            lx.eval('tool.attr gen.helix offset 0.0')
            if tolerance != '0':
                lx.eval('tool.attr effector.clone merge true')
                lx.eval('tool.attr effector.clone dist %s' % tolerance)
            else:
                lx.eval('tool.attr effector.clone merge false')
            lx.eval('tool.attr center.auto cenX 0.0')
            lx.eval('tool.attr center.auto cenY 0.0')
            lx.eval('tool.attr center.auto cenZ 0.0')
            lx.eval('tool.doApply')
            lx.eval('tool.drop')

        except Exception:
            lx.out(traceback.format_exc())
            lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')


    def basic_Enable(self,msg):
        return True

lx.bless(kelvin_quickRadial, "kelvin.quickRadial")
