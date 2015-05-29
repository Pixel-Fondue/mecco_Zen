#python

symmetry = lx.eval("select.symmetryState ?")

if symmetry!='none':
    lx.eval("tool.set symmetry.tool on")
    lx.eval("tool.setAttr symmetry.tool threshold 1000000000.0")
    lx.eval("tool.doApply")
    lx.eval("escape")
else:
    lx.eval("dialog.setup info")
    lx.eval("dialog.title {Symmetry not enabled.}")
    lx.eval("dialog.msg {Oops, make sure to enable symmetry.}")
    lx.eval("dialog.open")