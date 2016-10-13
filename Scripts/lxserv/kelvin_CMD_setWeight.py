#!/usr/bin/env python

import lx
import lxifc
import lxu
import lxu.command
import traceback

class kelvin_SetWeight(lxu.command.BasicCommand):

	def __init__(self):
		lxu.command.BasicCommand.__init__(self)

		self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
		self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

		self.dyna_Add('weight', lx.symbol.sTYPE_FLOAT)
		self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

	def basic_Execute(self, msg, flags):
		try:
			self.CMD_EXE(msg, flags)
		except Exception:
			lx.out(traceback.format_exc())
			lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

	def CMD_EXE(self, msg, flags):

		weight = self.dyna_String(0, 0.0)

		lx.eval('tool.set vertMap.setWeight on')
		lx.eval('tool.attr vertMap.setWeight weight %s' % weight)
		lx.eval('tool.doApply')

	def basic_Enable(self,msg):
		if self.activePolyCount() == 0:
			msg = lx.object.Message (msg)
			msg.SetCode (lx.result.CMD_DISABLED)
			msg.SetMessage("kelvinMessages", "kelvinMessages_1",140716001);
			return False
		else:
			return True

	def activePolyCount(self):
		layer_svc = lx.service.Layer ()
		layer_scan = lx.object.LayerScan (layer_svc.ScanAllocate (lx.symbol.f_LAYERSCAN_PRIMARY))
		if not layer_scan.test ():
			return

		layer_scan_count = layer_scan.Count ()
		if layer_scan_count == 0:
			return

		mesh_primary = lx.object.Mesh (layer_scan.MeshBase (0))
		if not mesh_primary.test ():
			return

		mesh_polygon_count    = mesh_primary.PolygonCount ()
		mesh_point_count    = mesh_primary.PointCount ()

		layer_scan.Apply ()

		return mesh_polygon_count

lx.bless(kelvin_SetWeight, "kelvin.setWeight")
