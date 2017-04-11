# python

import lx 
from zen import CommanderClass

CMD_NAME = 'zen.uiOrientation'

class CommandClass(CommanderClass):

    def commander_arguments(self):
        return [
                {
                    'name': 'action',
                    'label': 'Action',
                    'datatype': 'integer',
                    'default': 0,
                    'values_list_type': 'popup',
                    'values_list': ['toggle', 'right', 'left'],
                    'flags': [],
                },
                {
                    'name': 'value',
                    'label': 'Value',
                    'datatype': 'boolean',
                    'default': True,
                    'flags': ['optional', 'query'],
                }
                
            ]
            
    def commander_execute(self, msg, flags):
        if not self.commander_arg_value(0):
            return

        if self.commander_arg_value(0) == 0:
            newVal = not lx.eval("user.value right_handed ?")
        elif self.commander_arg_value(0) == 1:
            newVal = True
        else:
            newVal = False
            
        if newVal:
            lx.eval("viewport.hide False tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore zen6_toolboxes_mini_tag")
            lx.eval("viewport.hide False tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore zen6_toolboxes_miniFusion_tag")
            lx.eval("viewport.hide False tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore zen6_toolboxes_miniPaint_tag")
            lx.eval("viewport.hide False tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore zen6_toolboxes_miniSculpt_tag")
        else:
            lx.eval("viewport.hide False tag zen6_toolboxes_left_tag left zen6_toolboxes_tag_restore zen6_toolboxes_mini_tag")
            
        lx.eval("user.value right_handed %s" %str(newVal))

lx.bless(CommandClass, CMD_NAME)
