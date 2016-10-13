#python

import lx
import lxifc
import lxu

kelvin_CMD = "kelvin.setPsubLevel"

def is_enabled(cmd_string) :
    msg = lx.service.Message().Allocate()
    cmd = lx.service.Command().SpawnFromString(cmd_string)[2]
    try:
        cmd.Enable(msg)
    except RuntimeError, e:
        if e.message == 'bad result: CMD_DISABLED':
            return False
        raise
    return True

class ccsdsPopup(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items[0])

    def uiv_PopUserName(self,index):
        return self._items[1][index]

    def uiv_PopInternalName(self,index):
        return self._items[0][index]

class CmdChangePsubLevels(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('level', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def basic_ButtonName(self):
        return "Smoothness"

    def basic_Enable(self, msg):
        return True
#        if is_enabled('mesh.psubRenderSubdiv'):
#            return True
#        else:
#            return False

    def basic_Execute(self, msg, flags):
        l = self.dyna_Int(0) if self.dyna_IsSet(0) else 2
        try:
            lx.eval('!mesh.psubRenderSubdiv %s' % l)
        except:
            pass

        try:
            lx.eval('!mesh.psubSubdiv %s' % l)
        except:
            pass

        lx.eval('!mesh.patchSubdiv %s' % l)
        lx.eval('!mesh.renderSubdiv %s' % l)
        lx.eval('!mesh.spatchSubdiv %s' % (int(l)*8))

    def arg_UIValueHints(self, index):
        commands = [[],[]]
        for i in range(1,10):
            commands[0].append(str(i))
            commands[1].append("Level %s" % i)
        if index == 0:
            return ccsdsPopup(commands)

    def cmd_Query(self,index,vaQuery):
        va = lx.object.ValueArray()
        va.set(vaQuery)
        if index == 0:
                va.AddString(str(lx.eval('mesh.psubSubdiv ?')))
        return lx.result.OK

lx.bless(CmdChangePsubLevels, kelvin_CMD)
