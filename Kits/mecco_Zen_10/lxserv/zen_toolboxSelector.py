# python

import lx, lxifc, lxu
from zen import CommanderClass
from zen.Notifier import Notifier

CMD_NAME = 'zen.toolboxSelector'

TOOLBOXES = sorted([
    ('context', 'Context'),
    ('curves', 'Curves'),
    ('fusion', 'Fusion'),
    ('uv', 'UV'),
    ('paint', 'Paint'),
    ('sculpt', 'Sculpt'),
    ('animate', 'Animate'),
    ('game', 'Game'),
    ('actors', 'Actors'),
    ('deformers', 'Deformers'),
    ('dynamics', 'Dynamics'),
    ('particlePaint', 'Particle Paint'),
    ('vmap', 'Vertex Maps'),
    ('hair', 'Hair'),
    ('particles', 'Particles'),
    ('setup', 'Setup'),
    ('commandRegions', 'Command Regions'),
    ('ik', 'Inverse Kinematics'),
    ('topo', 'Retopology'),
    ('modifiers', 'Modifiers')
])

def form_command_list():
    fcl = []
    for toolbox in TOOLBOXES:
        fcl.append('zen.toolboxSelector {%s}' % toolbox[0])
    return fcl

class CommandClass(CommanderClass):
    def commander_arguments(self):
        return [
                {
                    'name': 'toolbox',
                    'datatype': 'string',
                    'values_list': TOOLBOXES,
                    'values_list_type': 'popup',
                    'flags': ['query'],
                }, {
                    'name': 'is_enabled',
                    'datatype': 'boolean',
                    'flags': ['query', 'optional', 'hidden'],
                }, {
                    'name': 'fcl',
                    'datatype': 'string',
                    'values_list': form_command_list,
                    'values_list_type': 'fcl',
                    'flags': ['query', 'optional', 'hidden'],
                }
            ]

    def commander_execute(self, msg, flags):
        lx.eval("user.value zen_current_toolbox %s" % self.commander_arg_value(0))

        notifier = Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_CHANGE_ALL)

    def commander_query(self, index):
        if index == 0:
            return lx.eval("user.value zen_current_toolbox ?")
        elif index == 1:
            toolbox_to_check = self.commander_arg_value(0)
            if lx.eval("user.value zen_current_toolbox ?") == toolbox_to_check:
                return True
            else:
                return False
        elif index == 2:
            return lx.result.OK

    def commander_notifiers(self):
        return [("zen.notifier", "")]

    def basic_ButtonName(self):
        toolbox_to_check = self.commander_args()['toolbox']
        if toolbox_to_check:
            for toolbox in TOOLBOXES:
                if toolbox[0] == toolbox_to_check:
                    return toolbox[1]

lx.bless(CommandClass, CMD_NAME)
