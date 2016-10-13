#!/usr/bin/env python

import lx
import lxifc
import lxu
import lxu.command
import traceback

def getItemsByType(intItemType):

    snSel = lxu.select.SceneSelection().current()

    itemCount = snSel.ItemCount(intItemType)
    items=[]

    for idx in range(itemCount):
        items.append(snSel.ItemByIndex(intItemType,idx))

    return items


class mapScan(lxifc.Visitor):

    def __init__(self, mesh,meshIdent):

        self.Ident = meshIdent
        self.mesh = mesh
        self.mapAccesssor = mesh.MeshMapAccessor()
        self.mapAccesssor.Enumerate(lx.symbol.iMARK_ANY,self,lx.object.Monitor())

    def vis_Evaluate(self):

        mapType = lxu.decodeID4(self.mapAccesssor.Type())

        if mapType == "NORM":
            #Remove is returning no access, so we are doing this the hard way :)
            lx.eval('!!select.item {%s} set' % self.Ident)
            lx.eval('!!select.vertexMap {%s} norm replace' % self.mapAccesssor.Name())
            lx.eval('!!vertMap.delete norm')


class kelvin_DeleteNormals(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())
            lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

    def CMD_EXE(self, msg, flags):
        meshes = getItemsByType(lx.symbol.i_CIT_MESH)
        for mesh in meshes:
            scene = mesh.Context()
            chan = scene.Channels(None,0.0)
            meshIdx = mesh.ChannelLookup(lx.symbol.sICHAN_MESH_MESH)
            mc = chan.ValueObj(mesh,meshIdx)
            mf = lx.object.MeshFilter(mc)
            genMesh = mf.Generate()
            mapVis = mapScan(genMesh,mesh.Ident())

    def basic_Enable(self,msg):
        return True

lx.bless(kelvin_DeleteNormals, "kelvin.removeNormals")
