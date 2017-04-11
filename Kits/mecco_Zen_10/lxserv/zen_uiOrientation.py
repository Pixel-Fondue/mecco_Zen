# python

import lx, lxifc, lxu
from zen import CommanderClass

CMD_NAME = 'zen.uiOrientation'

class CommandClass(CommanderClass):

    def commander_arguments(self):
        return [
                {
                    'name': 'action',
                    'label': 'Action',
                    'datatype': 'string',
                    'default': 'toggle',
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

        if self.commander_arg_value(0) == "toggle":
            newVal = not lx.eval("user.value right_handed ?")
        elif self.commander_arg_value(0) == "right":
            newVal = True
        else:
            newVal = False
            
  #      if newVal:
  #          lx.eval("viewport.hide False tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore zen6_toolboxes_mini_tag")
  #          lx.eval("viewport.hide False tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore zen6_toolboxes_miniFusion_tag")
  #          lx.eval("viewport.hide False tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore zen6_toolboxes_miniPaint_tag")
  #          lx.eval("viewport.hide False tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore zen6_toolboxes_miniSculpt_tag")
  #      else:
  #          lx.eval("viewport.hide False tag zen6_toolboxes_left_tag left zen6_toolboxes_tag_restore zen6_toolboxes_mini_tag")
            
        lx.out("cmd = ", "user.value right_handed %s" % int(newVal))
        lx.eval("user.value right_handed %s" % int(newVal))
        
        notifier = Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_CHANGE_ALL)
        
    def cmd_Query(self, index, vaQuery):

        # Create the ValueArray object
        va = lx.object.ValueArray()
        va.set(vaQuery)

        if index != 1:
            return lx.result.OK

        # GATHER VALUES
        # -------------

        action = self.commander_arg_value(0)

        if action == "right":
            va.AddInt(lx.eval("user.value right_handed ?"))
        elif action == "left":
            va.AddInt(not lx.eval("user.value right_handed ?"))
            
        return lx.result.OK
        
    def arg_UIValueHints(self, index):
        return cmd_Notifiers()
        
    def commander_notifiers(self):
        return [("zen.notifier", "")]
        
    def cmd_Flags (self):
        return lx.symbol.fCMD_UI | lx.symbol.fCMD_UNDO
        
class cmd_Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('zen.notifier',''),]
        
class Notifier(lxifc.Notifier):
    masterList = {}

    def noti_Name(self):
        return "zen.notifier"

    def noti_AddClient(self,event):
        self.masterList[event.__peekobj__()] = event

    def noti_RemoveClient(self,event):
        del self.masterList[event.__peekobj__()]

    def Notify(self, flags):
        for event in self.masterList:
            evt = lx.object.CommandEvent(self.masterList[event])
            evt.Event(flags)

lx.bless(Notifier, "zen.notifier")

lx.bless(CommandClass, CMD_NAME)
