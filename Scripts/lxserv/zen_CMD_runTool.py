#!/usr/bin/env python

import lx
import lxifc
import lxu
import lxu.command
import traceback
            
class zen_tool(lxu.command.BasicCommand):
    
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        
        # ARGUMENTS DEFINED HERE:
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)
        
        self.dyna_Add('tool', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
                
    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())
            lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')
        
    def CMD_EXE(self, msg, flags):
        
        # GRAB ARGUMENTS HERE:
        tool = self.dyna_String(0, 0.0)
    
        # CODE GOES HERE:
        lx.eval("tool.set %s on" % tool)
        lx.eval("tool.activate %s" % tool)
        lx.eval("tool.doApply")
        #lx.eval("tool.setAttr vertMap.setWeight showWeight true")
        lx.eval("attr.formPopover {toolprops:general}")
        
    def basic_Enable(self,msg):
        return True
        
lx.bless(zen_tool, "zen.tool")
    
