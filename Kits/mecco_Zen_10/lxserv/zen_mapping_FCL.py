# python

import lx, lxifc, lxu.command

FORMS = [
    {
        "label":"Zen Toolbox",
        "recommended": "V",
        "hash":"31757584531:sheet"
    }, {
        "label":"Zen Palettes List",
        "recommended": "G",
        "hash":"zen_palettesPopover:sheet"
    }, {
        "label":"Recent Tools",
        "recommended": "ctrl-R",
        "hash":"55281439258:sheet"
    }, {
        "label":"Workplane Pie",
        "recommended": "alt-W",
        "hash":"ZenPie_Workplane:sheet"
    }, {
        "label":"Snapping Pie",
        "recommended": "alt-X",
        "hash":"ZenPie_Snapping:sheet"
    }, {
        "label":"Falloff Pie",
        "recommended": "alt-F",
        "hash":"ZenPie_Falloff:sheet"
    }, {
        "label":"ActionCtr Pie",
        "recommended": "alt-A",
        "hash":"ZenPie_ActionCtr:sheet"
    }, {
        "label":"Layout Frames Pie",
        "recommended": "ctrl-shift-Space",
        "hash":"ZenPie_Frames:sheet"
    }
]

def list_commands():
    fcl = []
    for n, form in enumerate(sorted(FORMS, key=lambda k: k['label']) ):
        fcl.append("zen.labeledPopover {%s} {%s} {%s}" % (form["hash"], form["label"], form["recommended"]))
        fcl.append("zen.labeledMapKey {%s} {%s}" % (form["hash"], form["label"]))

        if n < len(FORMS)-1:
            fcl.append('- ')

    return fcl


class CommandListClass(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class CommandClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return CommandListClass(list_commands())

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(CommandClass, "zen.mapping_FCL")
