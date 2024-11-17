# python

import lx, lxifc, lxu
import zen

CMD_NAME = 'zen.uiOrientation'

def viewport_is_visible(tag, direction, restore_tag, tab_tag):
    return lx.eval('viewport.hide ? tag %s %s %s %s' % (tag, direction, restore_tag, tab_tag))

def safely_hide_viewport(tag, direction, restore_tag):
    if lx.eval('viewport.hide ? tag %s %s %s' % (tag, direction, restore_tag)):
        lx.eval('viewport.hide false tag %s %s %s' % (tag, direction, restore_tag))

def safely_show_viewport(tag, direction, restore_tag, tab_tag):
    if not lx.eval('viewport.hide ? tag %s %s %s %s' % (tag, direction, restore_tag, tab_tag)):
        lx.eval('viewport.hide true tag %s %s %s %s' % (tag, direction, restore_tag, tab_tag))

class CommandClass(zen.CommanderClass):
    def commander_arguments(self):
        return [
                {
                    'name': 'element',
                    'datatype': 'string',
                    'default': 'toolboxes'
                }, {
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
        element = self.commander_arg_value(0)
        right_handed = self.commander_arg_value(1)

        lx.eval("user.value right_handed_%s %s" % (element, int(right_handed)))

        if element == "toolboxes":
            frames = [
                {
                    'frame_tag_left': 'zen6_toolboxes_left_tag',
                    'frame_tag_right': 'zen6_toolboxes_right_tag',
                    'restore_tag_left': 'zen6_toolboxes_left_restore',
                    'restore_tag_right': 'zen6_toolboxes_right_restore',
                    'tab_tags': ["zen6_toolboxes_full_tag", "zen6_toolboxes_mini_tag", "zen6_toolboxes_miniFusion_tag", "zen6_toolboxes_miniPaint_tag", "zen6_toolboxes_miniSculpt_tag"]
                }
            ]

        else:
            frames = [
                {
                    'frame_tag_left': 'zen6_listviews_left_tag',
                    'frame_tag_right': 'zen6_listviews_right_tag',
                    'restore_tag_left': 'zen6_listviews_left_restore',
                    'restore_tag_right': 'zen6_listviews_right_restore',
                    'tab_tags': ["zen6_toolProperties_vpTag", "zen6_itemsTab_vpTag", "zen6_meshOpsTab_vpTag", "zen6_presetBrowserTab_vpTag"]
                }, {
                    'frame_tag_left': 'zen6_itemsTab_propsTabs_left_tag',
                    'frame_tag_right': 'zen6_itemsTab_propsTabs_right_tag',
                    'restore_tag_left': 'zen6_itemsTab_propsTabs_left_restore',
                    'restore_tag_right': 'zen6_itemsTab_propsTabs_right_restore',
                    'tab_tags': ["zen6_properties_vpGrp_tag", "zen6_channels_vpGrp_tag"]
                }
            ]

        for frame in frames:
            hide_frame_tag = frame['frame_tag_left'] if right_handed else frame['frame_tag_right']
            hide_restore_tag = frame['restore_tag_left'] if right_handed else frame['restore_tag_right']
            hide_direction = 'left' if right_handed else 'right'

            show_frame_tag = frame['frame_tag_right'] if right_handed else frame['frame_tag_left']
            show_restore_tag = frame['restore_tag_right'] if right_handed else frame['restore_tag_left']
            show_direction = 'right' if right_handed else 'left'

            current_tab_tag = None

            for tab_tag in frame['tab_tags']:
                if viewport_is_visible(hide_frame_tag, hide_direction, hide_restore_tag, tab_tag):
                    current_tab_tag = tab_tag
                    break

            safely_hide_viewport(hide_frame_tag, hide_direction, hide_restore_tag)

            if current_tab_tag is not None:
                safely_show_viewport(show_frame_tag, show_direction, show_restore_tag, current_tab_tag)

        notifier = zen.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_CHANGE_ALL)

    def commander_query(self, index):
        element = self.commander_arg_value(0)
        invert = self.commander_arg_value(2)

        if index == 1:
            if invert:
                return not lx.eval("user.value right_handed_%s ?" % element)
            else:
                return lx.eval("user.value right_handed_%s ?" % element)

    def commander_notifiers(self):
        return [("zen.notifier", "")]


lx.bless(CommandClass, CMD_NAME)
