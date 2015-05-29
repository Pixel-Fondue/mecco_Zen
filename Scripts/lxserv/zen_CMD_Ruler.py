#!/usr/bin/env python

################################################################################
#
# zen.ruler
#
# Version: 1.0
#
# Author: Tim Vazquez - CGM Studios
# Email: tim@cgmstudios.com
#
################################################################################
import lx
import lxu.command
import traceback


def setRuler(sX,sY,sZ,eX,eY,eZ):
    lx.eval('tool.setAttr util.ruler endX %s' % eX)
    lx.eval('tool.setAttr util.ruler endY %s' % eY)
    lx.eval('tool.setAttr util.ruler endZ %s' % eZ)
    lx.eval('tool.setAttr util.ruler startX %s' % sX)
    lx.eval('tool.setAttr util.ruler startY %s' % sY)
    lx.eval('tool.setAttr util.ruler startZ %s' % sZ)
    lx.eval('tool.doapply')


class newRuler(lxu.command.BasicCommand):
    
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)
        
        self.dyna_Add('eX', lx.symbol.sTYPE_FLOAT)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        
        self.dyna_Add('eY', lx.symbol.sTYPE_FLOAT)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)
        
        self.dyna_Add('eZ', lx.symbol.sTYPE_FLOAT)
        self.basic_SetFlags(3, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('sX', lx.symbol.sTYPE_FLOAT)
        self.basic_SetFlags(4, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('sY', lx.symbol.sTYPE_FLOAT)
        self.basic_SetFlags(5, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('sZ', lx.symbol.sTYPE_FLOAT)
        self.basic_SetFlags(6, lx.symbol.fCMDARG_OPTIONAL)

        
    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())
            lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')
        
    def CMD_EXE(self, msg, flags):
        
        sX = self.dyna_String(0, 0.0)
        sY = self.dyna_String(1, 0.0)
        sZ = self.dyna_String(2, 0.0)
        eX = self.dyna_String(3, 0.0)
        eY = self.dyna_String(4, 0.0)
        eZ = self.dyna_String(5, 0.0)
                    
        if lx.eval('tool.set util.ruler ?') != "on":
            lx.eval('tool.set util.ruler on')
            lx.eval('tool.activate util.ruler')
            
        setRuler(sX,sY,sZ,eX,eY,eZ)


    def basic_Enable(self,msg):
        return True
        
lx.bless(newRuler, "zen.ruler")

