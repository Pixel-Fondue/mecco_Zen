#python

if lx.eval('tool.set util.bounds ?') != "on":
    lx.eval('tool.set util.bounds on')
else:
    lx.eval("tool.set util.bounds off")

    
