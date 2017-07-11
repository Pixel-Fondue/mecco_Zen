# python

import lx, lxu, modo

NAME_CMD = "zen.dropEverything"

def setSelMode(mode):
    lx.eval('select.typeFrom %s;item;vertex;polygon;edge;pivot;center;ptag true' % mode)

def selMode():
    if lx.eval("select.typeFrom vertex;edge;polygon;item;pivot;center;ptag ?"):
        return 'vertex'

    elif lx.eval("select.typeFrom edge;vertex;polygon;item;pivot;center;ptag ?"):
        return 'edge'

    elif lx.eval("select.typeFrom polygon;vertex;edge;item;pivot;center;ptag ?"):
        return 'polygon'

    elif lx.eval("select.typeFrom ptag;vertex;polygon;item;pivot;center;edge ?"):
        return 'ptag'

    elif lx.eval("select.typeFrom item;vertex;polygon;edge;pivot;center;ptag ?"):
        return 'item'

    elif lx.eval("select.typeFrom pivot;vertex;polygon;item;edge;center;ptag ?"):
        return 'pivot'

    elif lx.eval("select.typeFrom center;vertex;polygon;item;pivot;edge;ptag ?"):
        return 'center'


class CMD_Zen(lxu.command.BasicCommand):

    def basic_Execute(self, msg, flags):
        mode = selMode()

        if lx.eval("user.value zen_dropEverything_selItem ?"):
            lx.eval('select.drop item')

        if lx.eval("user.value zen_dropEverything_selChannel ?"):
            lx.eval('select.drop channel')

        if lx.eval("user.value zen_dropEverything_selComponents ?"):
            lx.eval('select.drop polygon')
            lx.eval('select.drop edge')
            lx.eval('select.drop vertex')

        if lx.eval("user.value zen_dropEverything_Falloff ?"):
            lx.eval('tool.clearTask falloff')

        if lx.eval("user.value zen_dropEverything_Axis ?"):
            lx.eval('tool.clearTask axis')

        if lx.eval("user.value zen_dropEverything_Snap ?"):
            lx.eval('tool.clearTask snap')

        setSelMode(mode)

lx.bless(CMD_Zen, NAME_CMD)
