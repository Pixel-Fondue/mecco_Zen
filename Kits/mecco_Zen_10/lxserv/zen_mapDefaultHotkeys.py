# python

import lx, lxu, modo

HOTKEYS = [
    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "lock.sel"]
        ],
        "key":"j",
        "command":"vert.join false"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "layer.new"]
        ],
        "key":"n",
        "command":"layout.window ItemListAddPBViewPopover"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "layout_zen6_layout", None]
        ],
        "key":"ctrl-shift-space",
        "command":"attr.formPopover {ZenPie_Frames:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {82203601151:sheet}"]
        ],
        "key":"alt-backquote",
        "command":"viewport.maximize"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "edge.spinQuads"],
            [".global", "(stateless)", ".anywhere", ".itemMode", None]
        ],
        "key":"v",
        "command":"attr.formPopover {31757584531:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "viewport.goto"],
            ["IView", "(stateless)", ".anywhere", "(contextless)", "camera.goto"],
            ["view3DCamera", "(stateless)", ".anywhere", "(contextless)", "camera.goto"]
        ],
        "key":"g",
        "command":"attr.formPopover {zen_palettesPopover:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.drop"]
        ],
        "key":"q",
        "command":"zen.dropEverything"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "cmds.fireAgain uiCmds:false selectionCmds:false"]
        ],
        "key":"ctrl-r",
        "command":"attr.formPopover {55281439258:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.set actr.origin on"]
        ],
        "key":"alt-w",
        "command":"attr.formPopover [ZenPie_Workplane:sheet]"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.set actr.local on"]
        ],
        "key":"alt-x",
        "command":"attr.formPopover {ZenPie_Snapping:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.set actr.screen on"],
            ["view3DTools", "tool.ink.image", ".anywhere", "(contextless)", None]
        ],
        "key":"alt-f",
        "command":"attr.formPopover {ZenPie_Falloff:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.set actr.auto on"]
        ],
        "key":"alt-a",
        "command":"attr.formPopover {ZenPie_ActionCtr:sheet}"
    },

    {
        "contexts":[
            ["deformerList", "(stateless)", ".anywhere", "(contextless)", None],
            ["schematic", "(stateless)", ".anywhere", "(contextless)", None]
        ],
        "key":"enter",
        "command":"item.name"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "cmds.focusCommandEntry"],
            ["meshList", "(stateless)", ".anywhere", "(contextless)", None],
            ["meshList_inline", "(stateless)", ".anywhere", "(contextless)", None],
            ["meshList_slot", "(stateless)", ".anywhere", "(contextless)", None]
        ],
        "key":"enter",
        "command":"layer.renameSelected"
    },

    {
        "contexts":[
            ["shaderTree", "(stateless)", ".anywhere", "(contextless)", None]
        ],
        "key":"enter",
        "command":"texture.name"
    },

    {
        "contexts":[
            ["shaderTree", "(stateless)", ".anywhere", "(contextless)", None]
        ],
        "key":"ctrl-d",
        "command":"texture.duplicate"
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
        "command":"attr.formPopover {itemprops:general}"
    }

]


class CommandClass(lxu.command.BasicCommand):

    def cmd_Execute(self,flags):
        for hotkey in HOTKEYS:
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

        modo.dialogs.alert("Mapped Zen Hotkeys", "Mapped %s Zen hotkeys. See Zen documentation for details." % len(HOTKEYS))
        lx.eval("OpenURL {kit_mecco_zen:Documentation/hotkeys.html}")

lx.bless(CommandClass, "zen.mapDefaultHotkeys")


class RemoveCommandClass(lxu.command.BasicCommand):

    def cmd_Execute(self,flags):
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
