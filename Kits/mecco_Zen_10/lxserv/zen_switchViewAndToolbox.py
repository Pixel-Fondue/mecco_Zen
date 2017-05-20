# python

import lx, lxifc, lxu
import zen

CMD_NAME = 'zen.switchViewAndToolbox'

class CommandClass(zen.CommanderClass):
    def commander_arguments(self):
        return [
                {
                    'name': 'viewportTag',
                    'datatype': 'string'
                }, {
                    'name': 'toolboxName',
                    'datatype': 'string'
                }, {
                    'name': 'isLatest',
                    'datatype': 'boolean',
                    'flags': ['query', 'optional']
                }
            ]

    def commander_execute(self, msg, flags):
        try:
            lx.eval('viewport.tabWithTag %s' % self.commander_arg_value(0))
            lx.eval('zen.toolboxSelector %s' % self.commander_arg_value(1))
            lx.eval("user.value zen_latest_viewport %s" % self.commander_arg_value(0))
        except:
            pass

    def commander_query(self, index):
        if index == 2:
            return self.commander_arg_value(0) == lx.eval("user.value zen_latest_viewport ?")


lx.bless(CommandClass, CMD_NAME)
