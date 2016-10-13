#python

import modo, lx, symbols, items


def get_mode():
    """Returns the current selection mode as any of the following strings:
    vertex;edge;polygon;item;pivot;center;ptag
    """

    modes = 'vertex;edge;polygon;item;pivot;center;ptag'
    for mode in modes.split(';'):
        if lx.eval('select.typeFrom %s;%s ?' % (mode, modes)):
            return mode
    return False


def get_polys(connected=False):
    """Returns a list of all implicitly selected polys in all active layers.
    If in poly mode, returns selected polys. If in edge or vertex mode,
    returns all polys adjacent to all selected components.

    :param connected: If True, returns all polys connected to the selection."""

    result = set()
    scene = modo.scene.current()

    for layer in items.get_active_layers():

        if get_mode() == 'polygon':
            if layer.geometry.polygons.selected:
                for p in layer.geometry.polygons.selected:
                    result.add(p)
            else:
                for p in layer.geometry.polygons:
                    result.add(p)
        elif get_mode() == 'edge':
            if layer.geometry.edges.selected:
                for e in layer.geometry.edges.selected:
                    for p in e.polygons:
                        result.add(p)
            else:
                for p in layer.geometry.polygons:
                    result.add(p)
        elif get_mode() == 'vertex':
            if layer.geometry.edges.selected:
                for v in layer.geometry.vertices.selected:
                    for p in v.polygons:
                        result.add(p)
            else:
                for p in layer.geometry.polygons:
                    result.add(p)

        elif get_mode() == 'ptag':
            return False
        else:
            return False

        if connected:
            queue = list(result)
            island = set()

            while queue:
                poly = queue.pop()
                if not poly in island:
                    island.add(poly)
                    queue.extend( poly.neighbours )

            result = island

    return list(result)


def get_ptags(i_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL,connected=False):
    """Returns a list of all pTags for currently selected polys in all active layers.

    :param i_POLYTAG: type of tag to return (str), e.g. lx.symbol.i_POLYTAG_MATERIAL
    :param connected: extend selection to connected polys (bool)
    """

    r = set()
    pp = get_polys(connected)
    if pp:
        for p in pp:
            r.add(p.getTag(i_POLYTAG))
    return list(r)



def tag_polys(ptag,connected=False,i_POLYTAG=lx.symbol.i_POLYTAG_MATERIAL):
    """Assigns a pTag of type ptyp to all selected polys in all active layers.

    :param ptag: tag to apply (str)
    :param connected: extend selection to all connected polys (bool)
    :param ptyp: type of tag to apply (str) - e.g. lx.symbol.i_POLYTAG_MATERIAL
    """

    pp = get_polys(connected)
    if pp:
        for p in pp:
            if i_POLYTAG == lx.symbol.i_POLYTAG_PICK:
                tags = p.getTag(i_POLYTAG).split(";")
                if not ptag in tags:
                    tags.append(ptag)
                p.setTag(i_POLYTAG,";".join(tags))
            else:
                p.setTag(i_POLYTAG,ptag)

    mm = items.get_active_layers()
    for m in mm:
        m.geometry.setMeshEdits()

    return True
