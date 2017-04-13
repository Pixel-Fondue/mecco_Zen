# python

import lx, lxifc, lxu
from zen import CommanderClass

CMD_NAME = 'zen.uiOrientation'

class CommandClass(CommanderClass):
    def commander_arguments(self):
        return [
                {
                    'name': 'is_right_handed',
                    'datatype': 'boolean',
                    'default': True,
                    'flags': ['query'],
                }, {
                    'name': 'invert',
                    'datatype': 'boolean',
                    'default': False,
                    'flags': ['optional'],
                }
            ]

    def commander_execute(self, msg, flags):
        right_handed = self.commander_arg_value(0)

        lx.eval("user.value right_handed %s" % int(right_handed))

        tools = ["full_tag", "mini_tag", "miniFusion_tag", "miniPaint_tag", "miniSculpt_tag"]

        if right_handed:
            if lx.eval("viewport.hide ? tag zen6_presetBrowser_vpgrp_tag left zen6_upper_left_vptab_restore zen6_left_itemsTab_vpTag"):
                lx.eval("viewport.hide hide tag zen6_presetBrowser_vpgrp_tag left zen6_upper_left_vptab_restore zen6_left_itemsTab_vpTag")

            currentTool = None

            for tool in tools:
                if lx.eval("viewport.hide ? tag zen6_toolboxes_left_tag left zen6_toolboxes_tag_restore_left zen6_toolboxes_%s" % tool):
                    currentTool = tool

            if not lx.eval("viewport.hide ? tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore_right zen6_toolboxes_%s"% currentTool):
                lx.eval("viewport.hide true tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore_right zen6_toolboxes_%s"% currentTool)
                
            lx.eval("viewport.hide false tag zen6_toolboxes_left_tag left zen6_toolboxes_tag_restore_left")
        else:
            if lx.eval("viewport.hide ? tag zen6_presetBrowser_vpgrp_tag_dup right zen6_upper_right_vptab_restore_dup zen6_left_itemsTab_vpTag"):
                lx.eval("viewport.hide hide tag zen6_presetBrowser_vpgrp_tag_dup right zen6_upper_right_vptab_restore_dup zen6_left_itemsTab_vpTag")

            currentTool = None

            for tool in tools:
                if lx.eval("viewport.hide ? tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore_right zen6_toolboxes_%s" % tool):
                    currentTool = tool
                    
            if not lx.eval("viewport.hide ? tag zen6_toolboxes_left_tag left zen6_toolboxes_tag_restore_left zen6_toolboxes_%s"% currentTool):
                lx.eval("viewport.hide true tag zen6_toolboxes_left_tag left zen6_toolboxes_tag_restore_left zen6_toolboxes_%s"% currentTool)
                
            lx.eval("viewport.hide false tag zen6_toolboxes_right_tag right zen6_toolboxes_tag_restore_right")

        notifier = Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_CHANGE_ALL)

    def cmd_Query(self, index, vaQuery):
        invert = self.commander_arg_value(1)

        # Create the ValueArray object
        va = lx.object.ValueArray()
        va.set(vaQuery)

        if index == 0:
            if invert:
                va.AddInt(not lx.eval("user.value right_handed ?"))
            else:
                va.AddInt(lx.eval("user.value right_handed ?"))

        return lx.result.OK

    def arg_UIValueHints(self, index):
        return cmd_Notifiers()

    def commander_notifiers(self):
        return [("zen.notifier", "")]

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
