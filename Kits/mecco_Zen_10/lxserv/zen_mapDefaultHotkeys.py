# python

import lx, lxu, modo
from zen import CommanderClass

HOTKEYS = [
    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "lock.sel"]
        ],
        "key":"j",
        "command":"vert.join false",
        "name":"Vertex Join"
    },

    {
        "contexts":[
            ["view3DOverlay3D", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {27036209057:sheet}"]
        ],
        "key":"o",
        "command":"attr.formPopover {zen_viewportProperties_with_views:sheet}",
        "name":"Viewport Properties"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "layer.new"]
        ],
        "key":"n",
        "command":"layout.window ItemListAddPBViewPopover",
        "name":"New Item"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "layout_zen6_layout", None]
        ],
        "key":"ctrl-shift-space",
        "command":"zen.framesPie",
        "name":"Layout Frames Pie"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {82203601151:sheet}"]
        ],
        "key":"alt-backquote",
        "command":"viewport.maximize",
        "name":"Viewport Maximize"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "edge.spinQuads"],
            [".global", "(stateless)", ".anywhere", ".itemMode", None]
        ],
        "key":"v",
        "command":"attr.formPopover {31757584531:sheet}",
        "name":"Zen Toolbox"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "viewport.goto"],
            ["IView", "(stateless)", ".anywhere", "(contextless)", "camera.goto"],
            ["view3DCamera", "(stateless)", ".anywhere", "(contextless)", "camera.goto"]
        ],
        "key":"g",
        "command":"attr.formPopover {zen_palettesPopover:sheet}",
        "name":"Zen Palettes List"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.drop"]
        ],
        "key":"q",
        "command":"zen.dropEverything",
        "name":"Drop Everything"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "cmds.fireAgain uiCmds:false selectionCmds:false"]
        ],
        "key":"ctrl-r",
        "command":"attr.formPopover {55281439258:sheet}",
        "name":"Recent Tools"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.set actr.origin on"]
        ],
        "key":"alt-w",
        "command":"attr.formPopover [ZenPie_Workplane:sheet]",
        "name":"Workplane Pie"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.set actr.local on"]
        ],
        "key":"alt-x",
        "command":"attr.formPopover {ZenPie_Snapping:sheet}",
        "name":"Snapping Pie"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.set actr.screen on"],
            ["view3DTools", "tool.ink.image", ".anywhere", "(contextless)", None]
        ],
        "key":"alt-f",
        "command":"attr.formPopover {ZenPie_Falloff:sheet}",
        "name":"Falloffs Pie"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.set actr.auto on"]
        ],
        "key":"alt-a",
        "command":"attr.formPopover {ZenPie_ActionCtr:sheet}",
        "name":"Action Centers Pie"
    },

    {
        "contexts":[
            ["deformerList", "(stateless)", ".anywhere", "(contextless)", None],
            ["schematic", "(stateless)", ".anywhere", "(contextless)", None]
        ],
        "key":"enter",
        "command":"item.name",
        "name":"Item Rename"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "cmds.focusCommandEntry"],
            ["meshList", "(stateless)", ".anywhere", "(contextless)", None],
            ["meshList_inline", "(stateless)", ".anywhere", "(contextless)", None],
            ["meshList_slot", "(stateless)", ".anywhere", "(contextless)", None]
        ],
        "key":"enter",
        "command":"layer.renameSelected",
        "name":"Mesh Rename"
    },

    {
        "contexts":[
            ["shaderTree", "(stateless)", ".anywhere", "(contextless)", None]
        ],
        "key":"enter",
        "command":"texture.name",
        "name":"Texture Rename"
    },

    {
        "contexts":[
            ["shaderTree", "(stateless)", ".anywhere", "(contextless)", None]
        ],
        "key":"ctrl-d",
        "command":"texture.duplicate",
        "name":"Texture Duplicate"
    },

    {
        "contexts":[
            ["view3DSelect", "(stateless)", "item", "(contextless)", "attr.formPopover {itemprops:general}"],
            ["shaderTree", "(stateless)", ".anywhere", "(contextless)", None],
            ["deformerList", "(stateless)", ".anywhere", "(contextless)", None],
            ["schematic", "(stateless)", ".anywhere", "(contextless)", None],
            ["meshList", "(stateless)", "meshoperation", "(contextless)", None],
            ["meshList", "(stateless)", "deformName", "(contextless)", None],
            ["meshList", "(stateless)", "chanEffect", "(contextless)", None],
            ["meshList", "(stateless)", "chanModify", "(contextless)", None],
            ["meshList", "(stateless)", "itemModify", "(contextless)", None],
            ["meshList", "(stateless)", "itemRef", "(contextless)", None],
            ["meshList", "(stateless)", "cinemaRef", "(contextless)", None],
            ["meshList", "(stateless)", "cinemaName", "(contextless)", None]
        ],
        "key":"mmb",
        "command":"attr.formPopover {itemprops:general}",
        "name":"Item Properties"
    }

]


class CommandClass(CommanderClass):
    def commander_arguments(self):
        args = []
        for n, hotkey in enumerate(HOTKEYS):
            args.append({
                'name':str(n),
                'label':"%s \x03(c:25132927)(%s)" % (hotkey['name'], hotkey['key']),
                'datatype':'boolean',
                'default':True
            })
        return args

    def commander_execute(self, msg, flags):
        counter = 0
        for n, hotkey in enumerate(HOTKEYS):
            if not self.commander_arg_value(n):
                continue
            command = hotkey["command"]
            key = hotkey["key"]

            for context_list in hotkey["contexts"]:
                mapping = context_list[0]
                state = context_list[1]
                region = context_list[2]
                context = context_list[3]

                try:
                    lx.eval('!cmds.mapKey {%s} {%s} {%s} {%s} {%s} {%s}' % (key, command, mapping, state, region, context))
                except:
                    lx.out("Could not set '%s' to '%s'." % (command, key))

            counter += 1

        modo.dialogs.alert("Mapped Zen Hotkeys", "Mapped %s Zen hotkeys. See Help > Zen Hotkey Reference" % counter)

lx.bless(CommandClass, "zen.mapDefaultHotkeys")


class RemoveCommandClass(CommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in HOTKEYS:
            key = hotkey["key"]

            for context_list in hotkey["contexts"]:
                mapping = context_list[0]
                state = context_list[1]
                region = context_list[2]
                context = context_list[3]
                default = context_list[4]

                if default is None:
                    try:
                        lx.eval('!cmds.clearKey {%s} {%s} {%s} {%s} {%s}' % (key, mapping, state, region, context))
                    except:
                        lx.out("Could not clear mapping for '%s'." % key)
                else:
                    try:
                        lx.eval('!cmds.mapKey {%s} {%s} {%s} {%s} {%s} {%s}' % (key, default, mapping, state, region, context))
                    except:
                        lx.out("Could not set '%s' to '%s'." % (default, key))

        modo.dialogs.alert("Reverted Zen Hotkeys", "Reverted %s Zen hotkeys to defaults." % len(HOTKEYS))

lx.bless(RemoveCommandClass, "zen.unmapDefaultHotkeys")
