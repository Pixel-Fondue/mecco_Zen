#python 

lx.eval("tool.set prim.cylinder on") 
lx.eval("tool.attr prim.cylinder cenX 0.0") 
lx.eval("tool.attr prim.cylinder cenY 0.0") 
lx.eval("tool.attr prim.cylinder cenZ 0.0") 
lx.eval("tool.attr prim.cylinder sizeX 1.0")
lx.eval("tool.attr prim.cylinder sizeY 1.0")
lx.eval("tool.attr prim.cylinder sizeZ 1.0")
lx.eval("tool.enable")
lx.eval("attr.formPopover {toolprops:general}")

# #python

# lx.eval("tool.set WeightSelectAndGo on")
# lx.eval("tool.setAttr vertMap.setWeight showWeight true")
# lx.eval("attr.formPopover {toolprops:general}")