#python

vertList = lx.eval("query layerservice verts ? selected")
try:
    lx.eval("workPlane.reset")
    verta = lx.eval("query layerservice vert.wpos ? %s" % vertList[0])
    vertb = lx.eval("query layerservice vert.wpos ? %s" % vertList[1])
    lx.eval("cj.ruler %s %s %s %s %s %s" % (verta[0],verta[1],verta[2],vertb[0],vertb[1],vertb[2]))
except:
    #lx.eval("dialog.setup info")
    #lx.eval("dialog.msg {Select two vertices to measure.}")
    #lx.eval("dialog.open")
    lx.eval("tool.set util.ruler on snap:true")
    lx.eval("tool.doApply")