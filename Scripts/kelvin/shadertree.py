#python

import modo, lx, defaults, symbols, util, items


def build_material(
        item = None,
        i_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL,
        pTag = None,
        parent = None,
        name = None,
        overrides={},
        preset=None,
        shader=False
        ):

    """Builds a material in the shader tree, including a mask, material, and shader with default settings.

    :param item: item for mask to filter (optional)
    :type item: modo.item.Item() object

    :param i_POLYTAG: lx.symbol.i_POLYTAG_* (optional)
    :type i_POLYTAG: int

    :param pTag: pTag string (optional)
    :type pTag: str

    :param parent: parent (optional)
    :type parent: modo.item.Item() object

    :param name: name (optional)
    :type name: str

    :param name: overrides to merge with defaults (optional). For keys, see defaults.DEFAULTS
    :type name: dict

    :param preset: path to modo preset file (.lxp)
    :type preset: str

    :param shader: include shader in material group
    :type shader: bool
    """

    scene = modo.Scene()

    d = defaults.merge(overrides)
    color = util.random_color() if not 'color' in d else d['color']

    mask = add_mask(
        item,
        i_POLYTAG,
        pTag,
        parent,
        name
    )

    if parent:
        parent = get_masks(names = parent)[0]
        if parent:
            mask.setParent(parent,parent.childCount())

    if preset:
        pass

    if not preset:
        if(shader):
            sname = ' '.join([name,symbols.SHADERNAME]) if name else None
            channels = d['shader_channels']
            shdr = add_shader(sname,channels)
            shdr.setParent(mask)

        mname = ' '.join([name,symbols.MATNAME]) if name else None
        channels = d['material_channels']
        channels[lx.symbol.sICHAN_ADVANCEDMATERIAL_DIFFCOL] = color
        mat = add_material(mname,channels)
        mat.setParent(mask)

    return mask



def add_mask(
    item = None,
    i_POLYTAG = lx.symbol.i_POLYTAG_MATERIAL,
    pTag = None,
    parent = None,
    name = None
    ):

    """Add a Mask to the Shader Tree.

    :param item: item for mask to filter (optional)
    :type item: modo.item.Item() object

    :param i_POLYTAG: lx.symbol.i_POLYTAG_* (optional)
    :type i_POLYTAG: int

    :param pTag: pTag string (optional)
    :type pTag: str

    :param parent: parent (optional)
    :type parent: modo.item.Item() object

    :param name: name (optional)
    :type name: str
    """

    scene = modo.Scene()
    mask = scene.addItem(lx.symbol.sITYPE_MASK)

    if item:
        sg = scene.GraphLookup('shadeLoc')
        ig = lx.object.ItemGraph(sg)
        ig.AddLink(mask,item)

    if i_POLYTAG:
        mask.channel(lx.symbol.sICHAN_MASK_PTYP).set(symbols.sICHAN_MASK_PTYP(i_POLYTAG))

    if pTag:
        mask.channel(lx.symbol.sICHAN_MASK_PTAG).set(pTag)

    if not parent:
        parent = scene.renderItem
    elif get_masks(names=parent):
        mask.setParent(parent)

    mask.name = name if name else None

    return mask




def add_material(name=None,channels={}):
    """Adds a material item to the Shader Tree and sets channel values based on an optional dict."""

    scene = modo.scene.current()
    m = scene.addItem(lx.symbol.sITYPE_ADVANCEDMATERIAL, name)
    for k,v in channels.iteritems():
        m.channel(k).set(v)
    return m



def add_shader(name=None,channels={}):
    """Adds a shader item to the Shader Tree and sets channel values based on an optional dict."""

    scene = modo.scene.current()
    m = scene.addItem(lx.symbol.sITYPE_DEFAULTSHADER, name)
    for k,v in channels.iteritems():
        m.channel(k).set(v)
    return m



def seek_and_destroy(
    maskedItems = [],
    pTags = {},
    names = []
    ):

    """Remove all Shader Tree masks and eliminate pTags matching any of the provided criteria.

    :param maskedItems: remove item masks filtering any of the listed items
    :type maskedItems: list of modo.item.Item() objects

    :param pTags: remove masks filtering any of the "pTag":"i_POLYTAG" pairs
    :type pTags: dict of "pTag":lx.symbol.i_POLYTAG_* pairs
    """

    if not isinstance(maskedItems,list):
        maskedItems = [maskedItems]

    if not isinstance(names,list):
        names = [names]

    scene = modo.scene.current()

    if len(pTags) > 0:
        for m in scene.meshes:
            for p in m.geometry.polygons:
                for pTag, i_POLYTAG in pTags.iteritems():
                    if i_POLYTAG == lx.symbol.i_POLYTAG_PICK:
                        tags = p.getTag(i_POLYTAG).split(";")
                        tags.remove(pTag)
                        p.setTag(i_POLYTAG,";".join(tags))
                    else:
                        if p.getTag(i_POLYTAG) == pTag:
                            p.setTag(i_POLYTAG,defaults.get('ptag'))

    for i in get_masks(maskedItems,pTags,names):
        scene.removeItems(i,True)







def get_masks(
    maskedItems = [],
    pTags = {},
    names = []
    ):

    """Returns a list of all lx.symbol.sITYPE_MASK items given any of the provided criteria.

    :param maskedItems: items for which to find masks
    :type maskedItems: list of modo.item.Item() objects

    :param pTags: ptags for which to find masks
    :type pTags: dict of "pTag":lx.symbol.i_POLYTAG_* pairs

    :param names: UniqueNames for which to find masks
    :type names: list of strings to match with modo.item.Item().UniqueName()
    """

    if not isinstance(maskedItems,list):
        maskedItems = [maskedItems]

    if not isinstance(names,list):
        names = [names]

    scene = modo.Scene()

    r = set()
    for m in scene.iterItems(lx.symbol.sITYPE_MASK):
        maskedItem = get_masked_items(m)
        if maskedItem:
            if maskedItem in maskedItems:
                r.add(m)

        for pTag, pTyp in pTags.iteritems():
            if (
                m.channel(lx.symbol.sICHAN_MASK_PTYP).get() == symbols.sICHAN_MASK_PTYP(pTyp)
                and m.channel(lx.symbol.sICHAN_MASK_PTAG).get() == pTag
                ):

                r.add(m)

        if m.UniqueName() in names:
            r.add(m)

    return list(r)







def get_masked_items(
    masks=[]
    ):
    """Returns modo.item.Item() object(s) masked by the provided lx.symbol.sITYPE_MASK object(s).

    :param masks: mask objects for whom to list masked objects
    :type masks: object or list of objects
    """

    if not isinstance(masks,list):
        masks = [masks]

    sg = modo.Scene().GraphLookup('shadeLoc')
    ig = lx.object.ItemGraph(sg)

    r = set()
    for mask in masks:
        if ig.FwdCount(mask) > 0:
            r.add (modo.item.Item(ig.FwdByIndex(mask,0)))

    r = list(r)

    if len(r) == 1:
        return r[0]

    return r






def move_to_top(items):
    """Moves the supplied items to the top slot in their respective parents."""

    if not isinstance(items,list):
        items = [items]

    for item in items:
        item.setParent(item.parent,item.parent.childCount())




def get_shaders(mask):
    """Return a list of all shaders anywhere inside the supplied mask item."""

    shaders = set()
    for i in mask.children(True):
        if i.type == lx.symbol.sITYPE_DEFAULTSHADER:
            shaders.add(i)

    return list(shaders)



def get_environments(names):
    """Returns a list of environments matching any of the supplied uniqueNames."""

    scene = modo.Scene()

    if not isinstance(names,list):
        names = [names]

    return [e for e in scene.iterItems(lx.symbol.sITYPE_ENVIRONMENT) if e.name in names]



def add_environment(name=None,channels={}):
    """Adds an environment item and returns it."""

    scene = modo.scene.current()
    m = scene.addItem(lx.symbol.sITYPE_ENVIRONMENT, name)
    for k,v in channels.iteritems():
        m.channel(k).set(v)
    return m

def move_to_base_shader(items, above_base_shader=False):
    """Places supplied item(s) above or below Base Shader as appropriate.

    :param items: Item(s) to re-order
    :type items: modo.item.Item() object or list of the same

    :param above_base_shader: True if index should be above Base Shader (default: False)
    :type above_base_shader: bool"""

    if not isinstance(items,list):
        items = [items]

    for n, i in enumerate(modo.Scene().renderItem.children()):
    	if i.type == 'defaultShader':
    		target_index = n - 1

    if above_base_shader:
    	for n, i in enumerate(modo.Scene().renderItem.children()):
    		print n, i.name
    		if i.type == 'mask':
    			target_index = n if n > target_index else target_index + 1

    for item in items:
        item.setParent(modo.Scene().renderItem, target_index)
        return target_index

def cleanup():
    """Delete empty groups and unused polytag groups from Shader Tree."""

    scene = modo.scene.current()

    hitlist = set()
    for m in scene.iterItems(lx.symbol.sITYPE_MASK):

        if (m.parent.name == defaults.get_mask_group('ignore')):
            break

        # delete empty groups
        if not m.children():
            hitlist.add(m)

        i_POLYTAG = symbols.i_POLYTAG(m.channel(lx.symbol.sICHAN_MASK_PTYP).get()) # type of poly tag (material, selection set, etc)
        sICHAN_MASK_PTAG = m.channel(lx.symbol.sICHAN_MASK_PTAG).get() # poly tag ("myGreatMaterialTag")

        # delete obsolete (unused) polytag groups
        if (sICHAN_MASK_PTAG and not items.get_layers_by_pTag(sICHAN_MASK_PTAG,i_POLYTAG)):
            hitlist.add(m)

    for hit in hitlist:
        scene.removeItems(hit,True)

# def cleanup():
#     """Whip that shader tree into shape!
#     kelvin imposes a strict shader tree structure for usability and automation.
#     This function runs every time we do anything with the ST to maintain order in the universe.
#
#     - Adds HDR and Backplate environments if they don't already exist, and deletes any other environments
#     - Adds root level groups for item masks, group masks, polygon tag masks, etc
#     - Moves all existing masks to the appropriate root level groups above
#     - Removes empty masks groups (except the root ones above)
#     - Removes mask groups for unused ptags
#     - Removes mask groups that don't mask anything (except the root ones above)
#     - Completely ignores anything inside an "ignore" group at the root level (for advanced users)
#
#     Note: kelvin puts everything above the Base Shader, thereby requiring that all materials have a
#     dedicated Shader at the top. If a mask has no shader anywhere in its hierarchy, we'll add one.
#     If it has exactly one shader, we move it to the top. If it has more than one, we delete them
#     all and add a new one at the top to avoid confusion.
#     """
#
#     scene = modo.scene.current()
#
#     for e in reversed(defaults.get_environments()):
#         if not get_environments(e[1]):
#             add_environment(e[1],e[2])
#
#     for n in scene.items(lx.symbol.sITYPE_ENVIRONMENT):
#         if n.name not in [e[1] for e in defaults.get_environments()]:
#             scene.removeItems(n,True)
#
#     for groupName in reversed(defaults.get_mask_groups()):
#
#         if not get_masks(names=groupName):
#             add_mask(name=groupName)
#
#         get_masks(names=groupName)[0].setParent(scene.renderItem)
#         move_to_top(get_masks(names=groupName)[0])
#
#         if groupName == defaults.get_mask_group('base'):
#             mask = get_masks(names=groupName)[0]
#
#             if not mask.children():
#                 sname = symbols.BASE_SHADER
#                 channels = defaults.get('shader_channels')
#                 shdr = add_shader(sname,channels)
#                 shdr.setParent(mask)
#
#                 mname = symbols.BASE_MATERIAL
#                 channels = defaults.get('material_channels')
#                 channels[lx.symbol.sICHAN_ADVANCEDMATERIAL_DIFFCOL] = defaults.get('base_material_color')
#                 mat = add_material(mname,channels)
#                 mat.setParent(mask)
#
#
#     hitlist = set()
#     for m in scene.iterItems(lx.symbol.sITYPE_MASK):
#
#         if (
#             not m.parent.name == defaults.get_mask_group('ignore')
#             and not m.name in defaults.get_mask_groups()
#             ):
#
#             parentName = None
#             i_POLYTAG = symbols.i_POLYTAG(m.channel(lx.symbol.sICHAN_MASK_PTYP).get())
#
#             if not m.children():
#                 hitlist.add(m)
#
#             elif (
#                 m.channel(lx.symbol.sICHAN_MASK_PTAG).get()
#                 and not items.get_layers_by_pTag(
#                     m.channel(lx.symbol.sICHAN_MASK_PTAG).get(),
#                     i_POLYTAG
#                     )
#                 ):
#                 hitlist.add(m)
#
#             elif lx.symbol.sGRAPH_SHADELOC in m.itemGraphNames:
#
#                 maskedItemType = m.itemGraph(lx.symbol.sGRAPH_SHADELOC).forward()[0].type
#
#                 if maskedItemType == '':
#                     parentName = defaults.get_mask_group('group')
#
#                 elif maskedItemType == lx.symbol.sITYPE_GROUPLOCATOR:
#                     parentName = defaults.get_mask_group('gloc')
#
#                 else:
#                     parentName = defaults.get_mask_group('item')
#
#             elif i_POLYTAG == lx.symbol.i_POLYTAG_MATERIAL:
#                 parentName = defaults.get_mask_group('ptag')
#
#             elif i_POLYTAG == lx.symbol.i_POLYTAG_PICK:
#                 parentName = defaults.get_mask_group('selset')
#
#             elif i_POLYTAG == lx.symbol.i_POLYTAG_PART:
#                 parentName = defaults.get_mask_group('part')
#
#             else:
#                 hitlist.add(m)
#
#
#             if parentName and not m.parent.name == parentName:
#                 m.setParent(get_masks(names=parentName)[0])
#
#
#             shaders = get_shaders(m)
#             if len(shaders) == 0:
#                 s = add_shader()
#                 s.setParent(m,m.childCount())
#             elif len(shaders) == 1:
#                 shaders[0].setParent(m,m.childCount())
#             else:
#                 for shader in shaders:
#                     scene.removeItems(shader,True)
#                 s = add_shader()
#                 s.setParent(m,m.childCount())
#
#
#     for i in scene.renderItem.children():
#         if i.type == lx.symbol.sITYPE_RENDEROUTPUT:
#             i.setParent(get_masks(names=defaults.get_mask_group('output'))[0])
#         elif (
#             i.type == lx.symbol.sITYPE_DEFAULTSHADER
#             or i.type == lx.symbol.sITYPE_ADVANCEDMATERIAL
#             ):
#             scene.removeItems(i)
#
#
#     for m in scene.iterItems(lx.symbol.sITYPE_MASK):
#         if not m.children() and not m.name == defaults.get_mask_group('ignore'):
#                 hitlist.add(m)
#
#
#     for hit in hitlist:
#         scene.removeItems(hit,True)
