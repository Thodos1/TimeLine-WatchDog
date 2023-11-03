"""

Author: Maksym Vysokolov
Website: cataclysm-vfx.com

License: GPLv3

"""
import os, sys
import re
from collections import defaultdict
import c4d
from c4d import gui

def load_bitmap(path):
	path = os.path.join(os.path.dirname(__file__), path)
	bmp = c4d.bitmaps.BaseBitmap()
	if bmp.InitWith(path)[0] != c4d.IMAGERESULT_OK:
		bmp = None
	return bmp

PLUGIN_ID = 1061347
PLUGIN_NAME = 'TimeLine Watchdog'
PLUGIN_ICON = load_bitmap('res/Watchdog_ico.tif')
PLUGIN_INFO = 0
PLUGIN_HELP = 'Update timeline to Render Settings'

class TextureSetsDialog(gui.GeDialog):
	def Action_rend_override(self):
		doc = c4d.documents.GetActiveDocument()
		rd_a = doc.GetActiveRenderData()

		rdFrom_a = rd_a[c4d.RDATA_FRAMEFROM].GetFrame(c4d.documents.GetActiveDocument().GetFps())
		rdTo_a   = rd_a[c4d.RDATA_FRAMETO].GetFrame(c4d.documents.GetActiveDocument().GetFps())
		if self.GetBool(3000) == True:
			doc.SetMinTime(c4d.BaseTime(rdFrom_a, doc.GetFps())) # Set the start frame to 12
			doc.SetMaxTime(c4d.BaseTime(rdTo_a, doc.GetFps()))


		doc.SetLoopMinTime(rd_a[c4d.RDATA_FRAMEFROM])
		doc.SetLoopMaxTime(rd_a[c4d.RDATA_FRAMETO])
		if self.GetBool(3003) == True:
			time_t = c4d.BaseTime(rdFrom_a, doc.GetFps())
			doc.SetTime(time_t)


		self.SetString(100230, self.Rendsets())
		self.LayoutChanged(100230)
		c4d.EventAdd()



	def Rendsets(self):
		doc = c4d.documents.GetActiveDocument()
		rd = doc.GetActiveRenderData()

		rdFrom = rd[c4d.RDATA_FRAMEFROM].GetFrame(c4d.documents.GetActiveDocument().GetFps())
		rdTo   = rd[c4d.RDATA_FRAMETO].GetFrame(c4d.documents.GetActiveDocument().GetFps())

		ret_dat = (f"{rdFrom}f - {rdTo}f")
		return ret_dat

	def CreateLayout(self):

		self.SetTitle("Render Settings Watchdog")

		self.GroupBegin(3232, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=0, rows=2)



		self.GroupBegin(id=1001, flags=c4d.BFH_CENTER | c4d.BFV_SCALEFIT, cols=0, rows=0)
		self.GroupBorder(c4d.BORDER_IN)

		self.AddStaticText(100230, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, name=self.Rendsets())




		self.GroupEnd()
		self.GroupBegin(3235, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=0, rows=2)
		self.AddCheckbox(3000, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 0, 0, name="Frame Range Override")
		self.AddCheckbox(3003, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 0, 0, name="Playhead Override")
		self.SetBool(3000, True)
		self.SetBool(3003, True)
		self.GroupEnd()
		self.GroupEnd()
		return True

	def Command(self, id, msg):
		return True

	def CoreMessage(self, id, msg):
		#RENDER CHANGE ID
		if id == 1970300013 or id == 1952671847:
			self.Action_rend_override()




		return True
"""

1970300013 this looks like a render document id


"""



class TL_Watch(c4d.plugins.CommandData):
	dialog = None

	def Execute(self, doc):
		# create the dialog
		if self.dialog is None:



			self.dlg = TextureSetsDialog()
		return self.dlg.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, xpos=-1, ypos=-1)

# # Open the dialog
# dlg_mul = TextureSetsDialog()
# dlg_mul.Open(dlgtype=c4d.DLG_TYPE_ASYNC)
if __name__ == "__main__":
	exec_plug = c4d.plugins.RegisterCommandPlugin(PLUGIN_ID, PLUGIN_NAME, PLUGIN_INFO, PLUGIN_ICON, PLUGIN_HELP,
												  TL_Watch())
	if (exec_plug):
		print("TimeLine Watchdog registered successfully")
