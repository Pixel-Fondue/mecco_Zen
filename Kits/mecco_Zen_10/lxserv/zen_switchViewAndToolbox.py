# python

import lx, lxifc, lxu
from zen import CommanderClass
from zen.Notifier import Notifier

CMD_NAME = 'zen.switchViewAndToolbox'

class CommandClass(CommanderClass):
    def commander_arguments(self):
        return [
                {
                    'name': 'viewportTag',
                    'datatype': 'string'
                }, {
                    'name': 'toolboxName',
                    'datatype': 'string'
                }
            ]

    def commander_execute(self, msg, flags):
        try:
            lx.eval('viewport.tabWithTag %s' % self.commander_arg_value(0))
            lx.eval('zen.toolboxSelector %s' % self.commander_arg_value(1))
        except:
            pass


lx.bless(CommandClass, CMD_NAME)
