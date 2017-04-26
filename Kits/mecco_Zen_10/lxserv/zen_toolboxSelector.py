# python

import lx, lxifc, lxu
from zen import CommanderClass
from zen import Notifier

CMD_NAME = 'zen.toolboxSelector'

TOOLBOXES = sorted([
    ('context', 'Context'),
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
    ('ik', 'Inverse Kinematics')
])

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
                    'name': 'enable',
                    'datatype': 'boolean',
                    'default': False,
                    'flags': ['query'],
                }
            ]

    def commander_execute(self, msg, flags):
        right_handed = self.commander_arg_value(0)

        notifier = Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_CHANGE_ALL)

    def commander_query(self, index):
        if index == 0:
            return True
        elif index == 1:
            self.commander_arg_value(0)

        return lx.result.OK

    def commander_notifiers(self):
        return [("zen.notifier", "")]

lx.bless(CommandClass, CMD_NAME)
