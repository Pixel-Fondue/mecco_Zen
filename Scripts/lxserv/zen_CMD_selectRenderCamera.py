#!/usr/bin/env python

import lx
import lxifc
import lxu
import lxu.command
import traceback
            
class zen_selectRenderItem(lxu.command.BasicCommand):
    
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
                
    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())
            lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')
        
    def CMD_EXE(self, msg, flags):
    
        # CODE GOES HERE:
        scene = lxu.select.SceneSelection().current()
        renderObject = scene.AnyItemOfType(lx.symbol.i_CIT_RENDER)
        lx.eval('select.item {%s} set' % renderObject.Ident())
        renderCamera = lx.eval("render.camera ?")
        lx.eval('select.item {%s} add' % renderCamera)
        
        
    def basic_Enable(self,msg):
        return True
        
lx.bless(zen_selectRenderItem, "zen.selectRenderItem")
    
