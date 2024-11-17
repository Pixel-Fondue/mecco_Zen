# python

import lx, lxifc, lxu
import zen

CMD_NAME = 'zen.miniToolboxVisibility'

def viewport_is_visible(tag, direction, restore_tag):
    return lx.eval('viewport.hide ? tag %s %s %s' % (tag, direction, restore_tag))

def safely_hide_viewport(tag, direction, restore_tag):
    if viewport_is_visible(tag, direction, restore_tag):
        lx.eval('viewport.hide false tag %s %s %s' % (tag, direction, restore_tag))

def safely_show_viewport(tag, direction, restore_tag):
    if not viewport_is_visible(tag, direction, restore_tag):
        lx.eval('viewport.hide true tag %s %s %s' % (tag, direction, restore_tag))

class CommandClass(zen.CommanderClass):
    def commander_arguments(self):
        return [
                {
                    'name': 'visible',
                    'datatype': 'boolean',
                    'flags': ['query']
                }
            ]

    def commander_execute(self, msg, flags):
        enable = self.commander_arg_value(0)
        side = 'right' if lx.eval("user.value right_handed_toolboxes ?") else 'left'

        if enable:
            safely_show_viewport('zen6_toolboxes_%s_tag' % side, side, 'zen6_toolboxes_%s_restore' % side)
        else:
            safely_hide_viewport('zen6_toolboxes_%s_tag' % side, side, 'zen6_toolboxes_%s_restore' % side)

        notifier = zen.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_CHANGE_ALL)

    def commander_query(self, index):
        if index == 0:
            side = 'right' if lx.eval("user.value right_handed_toolboxes ?") else 'left'
            return viewport_is_visible('zen6_toolboxes_%s_tag' % side, side, 'zen6_toolboxes_%s_restore' % side)

    def commander_notifiers(self):
        return [("zen.notifier", "")]

lx.bless(CommandClass, CMD_NAME)
