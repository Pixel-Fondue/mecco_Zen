# python

import lx, modo, lxu.command, traceback, os, re

CMD_NAME = 'zen.startup'

class myGreatCommand(lxu.command.BasicCommand):

    def CMD_EXE(self, msg, flags):
        zen_version_from_config = lx.eval("user.value zen_version ?")

        kit_folder = lx.eval("query platformservice alias ? {kit_mecco_zen:}")
        index_file = os.path.join(kit_folder, "index.cfg")

        # xml.etree is not included in MODO install, so we need a hack
        # index_xml = xml.etree.ElementTree.parse(index_file).getroot()
        # zen_version_installed = index_xml.attrib["version"]

        # Regex is hardly ideal for this. But it works in the absense of an XML parser.
        with open(index_file, 'r') as index_file_data:
            xml_as_string = index_file_data.read().replace('\n', '')

        r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
        m = re.search(r, xml_as_string)
        zen_version_installed = m.group(1)

        if not zen_version_from_config:
            modo.dialogs.alert(
                "New Zen Install",
                "New install of Zen detected. Set hotkeys and other prefs: Preferences > Mechanical Color > Zen UI\nSee 'Help > Zen Release Notes' for more."
                )
            lx.eval('layout.window Preferences')
            lx.eval('pref.select mecco/zen_ui_prefs set')

        elif zen_version_from_config != zen_version_installed:
            modo.dialogs.alert(
                "New Zen Version",
                "IMPORTANT: New version of Zen detected. Reset MODO prefs using:\nSystem > Reset Preferences"
                )

        lx.eval("user.value zen_version %s" % zen_version_installed)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

lx.bless(myGreatCommand, CMD_NAME)
