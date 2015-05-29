#!/usr/bin/env python

import lx
import lxifc
import lxu
import lxu.command
import traceback
			
class zen_setRef(lxu.command.BasicCommand):
	
	def __init__(self):
		lxu.command.BasicCommand.__init__(self)
		
		# ARGUMENTS DEFINED HERE:
		self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
		self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)
		
		# First we need to make this argument type a BOOLEAN
		self.dyna_Add('active', lx.symbol.sTYPE_BOOLEAN)
		self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY)
				
	def basic_Execute(self, msg, flags):
		try:
			self.CMD_EXE(msg, flags)
		except Exception:
			lx.out(traceback.format_exc())
			lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')
		
	def CMD_EXE(self, msg, flags):
		
		# GRAB ARGUMENTS HERE:
		if self.dyna_String(0, 0.0):
			active = self.dyna_String(0, 0.0)
		else:
			active = 0
	
		# CODE GOES HERE:
		# See if the user value exists
		if lx.eval("query scriptsysservice userValue.isDefined ? zen_setRef")==0:
			lx.eval( 'user.defNew zen_setRef boolean' );
			lx.eval( 'user.def zen_setRef username value:0' );
			
		zen_setRef = lx.eval('user.value zen_setRef ?')
		  
		if zen_setRef==0:
			try:
				lx.eval('item.refSystem')
				lx.eval('user.value zen_setRef 1')
			except Exception:
				lx.eval('user.value zen_setRef 0')
				lx.eval('dialog.setup info')
				lx.eval('dialog.title {Oops.}')
				lx.eval('dialog.msg {Please select at least one item to setRef.}')
				lx.eval('dialog.open')
		else:
			try:
				lx.eval('item.refSystem {}')
				lx.eval('user.value zen_setRef 0')
			except Exception:
				lx.eval('user.value zen_setRef 1')
				lx.eval('dialog.setup info')
				lx.eval('dialog.msg {Oops. Something funny is going on here.}')
				lx.eval('dialog.open')
	
	def checkState(self):
		if lx.eval("query scriptsysservice userValue.isDefined ? zen_setRef")==0:
			lx.eval( 'user.defNew zen_setRef boolean' );
			lx.eval( 'user.def zen_setRef username value:0' );
		return int(lx.eval('user.value zen_setRef ?'))
	
	def cmd_Query(self,index,va):

		if index == 1:
			# The active argument is at index 1
			zen_setRef = self.checkState()
			
			# we now cast the unknown object to a Value array object
			# and add an int value of 0 or 1
			valObj = lx.object.ValueArray(va)
			valObj.AddInt(zen_setRef)

				
	def basic_Enable(self,msg):
		return True
		
lx.bless(zen_setRef, "zen.setRef")
	
