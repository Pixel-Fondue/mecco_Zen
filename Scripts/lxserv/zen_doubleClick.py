# python

import lx, lxu, modo

NAME_CMD = "zen.doubleClick"

def selectedIsMesh():
    try:
        return modo.Scene().selected[-1].type == 'mesh'
    except IndexError:
        return False

def setItemMode():
    lx.eval('select.typeFrom item;vertex;polygon;edge;pivot;center;ptag true')

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


class CMD_Zen_doubleClick(lxu.command.BasicCommand):

    def basic_Execute(self, msg, flags):
        if not lx.eval('user.value mecco_zen.doubleClick ?'):
            return lx.symbol.e_OK

        if selMode() == 'item':
            if selectedIsMesh():
                lx.eval("select.typeFrom polygon;vertex;edge;item;pivot;center;ptag true")
            else:
                lx.eval("select.itemHierarchy")
        elif selMode() == 'polygon':
            if lx.eval("query layerservice polys ? selected"):
                lx.eval("select.connect")
            else:
                setItemMode()
        elif selMode() == 'edge':
            if lx.eval("query layerservice edges ? selected"):
                lx.eval("select.loop")
            else:
                setItemMode()
        elif selMode() == 'vertex':
            if lx.eval("query layerservice verts ? selected"):
                lx.eval("select.connect")
            else:
                setItemMode()



lx.bless(CMD_Zen_doubleClick, NAME_CMD)
