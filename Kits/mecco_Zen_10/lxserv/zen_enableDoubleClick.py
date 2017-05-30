# python

import lx, lxu, modo
import zen

class CommandClass(zen.CommanderClass):

    def commander_arguments(self):
        return [
                {
                    'name': 'enabled',
                    'label': 'Enable Zen Double-Click',
                    'datatype': 'boolean',
                    'default': False,
                    'flags': ['query']
                }
            ]

    def commander_execute(self, msg, flags):

        if self.commander_arg_value(0):

            safety = modo.dialogs.yesNo("Not Recommended", "Zen Double-Click has unresolved problems, and it's currently not recommended. Are you sure you want to use it?")

            if safety == "no":
                return

            command = "zen.doubleClick"
            key = "lmb-dblclick"
            mapping = "view3DSelect"
            state = "(stateless)"
            region = ".anywhere"
            context = "(contextless)"

            lx.eval('!cmds.mapKey {%s} {%s} {%s} {%s} {%s} {%s}' % (key, command, mapping, state, region, context))
            lx.eval('pref.value opengl.mouseRegionsSelect false')

            lx.eval("user.value zen_double_click true")

            modo.dialogs.alert("Mapped Zen Double-Click", "Double-click in a 3D viewport\nis now mapped to 'zen.doubleClick', and\nPreferences > OpenGL > Selection > Mouse Regions Trigger Selection\nis now disabled.")
            lx.eval("OpenURL {kit_mecco_zen:Documentation/doubleclick.html}")

        else:

            command = ""
            key = "lmb-dblclick"
            mapping = "view3DSelect"
            state = "(stateless)"
            region = ".anywhere"
            context = "(contextless)"

            lx.eval('!cmds.clearKey {%s} {%s} {%s} {%s} {%s}' % (key, mapping, state, region, context))
            lx.eval('pref.value opengl.mouseRegionsSelect true')

            lx.eval("user.value zen_double_click false")

            modo.dialogs.alert("Mapped Zen Double-Click", "Zen Double-Click has been disabled, and \nPreferences > OpenGL > Selection > Mouse Regions Trigger Selection\nis now enabled.")

    def commander_query(self, index):
        if index == 0:
            return lx.eval("user.value zen_double_click ?")

lx.bless(CommandClass, "zen.zenDoubleClick")
