# python

import lx, modo, os, re
from zen import CommanderClass

CMD_NAME = 'zen.startup'

class myGreatCommand(CommanderClass):

    def commander_execute(self, msg, flags):
        zen_version_from_config = lx.eval("user.value zen_version ?")

        kit_folder = lx.eval("query platformservice alias ? {kit_mecco_zen:}")
        index_file = os.path.join(kit_folder, "index.cfg")

        # xml.etree is not included in MODO install, so we need a hack
        # index_xml = xml.etree.ElementTree.parse(index_file).getroot()
        # zen_version_installed = index_xml.attrib["version"]

        # Regex is hardly ideal for this. But it works in the absence of an XML parser.
        with open(index_file, 'r') as index_file_data:
            xml_as_string = index_file_data.read().replace('\n', '')

        r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
        m = re.search(r, xml_as_string)
        zen_version_installed = m.group(1)

        if not zen_version_from_config:
            lx.eval('zen.mapDefaultHotkeys')

        elif zen_version_from_config != zen_version_installed:
            modo.dialogs.alert(
                "New Zen Version",
                "IMPORTANT: New version of Zen detected. Reset MODO prefs using:\nSystem > Reset Preferences"
                )

        lx.eval("user.value zen_version %s" % zen_version_installed)

lx.bless(myGreatCommand, CMD_NAME)
