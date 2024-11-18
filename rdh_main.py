import renderdoc as rd
import qrenderdoc as qrd

import PySide2
from PySide2 import QtCore, QtWidgets, QtGui


class MainData():
    def __init__(self) -> None:
        self.meshes_data: list = []
        self.textures_data: list = []

    def CLearData(self):
        self.meshes_data.clear()
        self.textures_data.clear()


class RDHCaptureViewer(qrd.CaptureViewer):
    def __init__(self, ctx: qrd.CaptureContext, version: str):
        super().__init__()

        self.ctx: qrd.CaptureContext = ctx
        self.version: str = version
        
        self.main_widget: MainWidget = MainWidget()

        self.main_data = MainData()

        # TEST TEST TEST TEST
        self.testPrint = QtWidgets.QMessageBox()

        ########## FINAL THINGS
        ctx.AddDockWindow(self.main_widget, qrd.DockReference.MainToolArea, None)
        ctx.AddCaptureViewer(self)

    ### qrd.CaptureViewer Functions
    def OnCaptureLoaded(self):
        self.main_data.CLearData()
        self.main_widget.ClearUI()

    def OnCaptureClosed(self):
        self.main_data.CLearData()
        self.main_widget.ClearUI()

    def OnSelectedEventChanged(self, event):
        pass

    def OnEventChanged(self, event):
        pass

    ### RDHCaptureViewer Functions
    def UpdateData(self):
        self.main_data.CLearData()
        self.ctx.Replay().BlockInvoke(self.UpdateDataWithReplay)
        
        self.main_widget.UpdateUI()
        
        self.testPrint.setText(str(len(self.main_data.meshes_data)) + "  " + str(len(self.main_data.textures_data)))
        self.testPrint.show()

    def UpdateDataWithReplay(self, r_ctrl: rd.ReplayController):
        startEID: int = self.main_widget.GetStartEID()
        endEID: int = self.main_widget.GetEndEID()

        # Check
        if (startEID < 0 or endEID < 1) or endEID <= startEID:
            return

        for i, res in enumerate(self.ctx.GetResources()):
            res_id = res.resourceId
            usages = r_ctrl.GetUsage(res_id)

            if res.type == rd.ResourceType.Texture:
                tex = self.ctx.GetTexture(res_id)

                for use in usages:
                    event_id: int = use.eventId

                    # Check
                    if event_id < startEID or event_id > endEID:
                        continue

                    if usages and tex.type == rd.TextureType.Texture2D:
                        tex_width: int = tex.width
                        tex_height: int = tex.height
                        tex_size = max(tex_width, tex_height)

                        if tex_size >= 128:
                            self.main_data.textures_data.append((event_id, tex_width,
                                                                tex_height, tex_size, i))
                            
                            if self.main_widget.uniques_textures_checkbox.isChecked():
                                break

            elif res.type == rd.ResourceType.Buffer:
                buf = the_window.ctx.GetBuffer(res_id)
                if 'Index' in str(buf.creationFlags):
                    for use in usages:
                        event_id: int = use.eventId

                        # Check
                        if event_id < startEID or event_id > endEID:
                            continue

                        if use.usage == rd.ResourceUsage.IndexBuffer:
                            action: rd.ActionDescription = self.ctx.GetAction(event_id)

                            if action.numIndices and action.numIndices >= 3:
                                # index_offset = action.indexOffset
                                triangles_num = int(action.numIndices / 3)

                                self.main_data.meshes_data.append((event_id, triangles_num, i))

                                if self.main_widget.uniques_meshes_checkbox.isChecked():
                                    break

        if self.main_data.textures_data:
            self.main_data.textures_data.sort(key=lambda value: value[3], reverse=True)

        if self.main_data.meshes_data:
            self.main_data.meshes_data.sort(key=lambda value: value[1], reverse=True)

the_window: RDHCaptureViewer = None

class MainWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('RDHelper')

        self.main_container: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout(self)

        self.left_main_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.left_main_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.right_main_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()

        self.main_container.addLayout(self.left_main_layout, stretch=1)
        self.main_container.addLayout(self.right_main_layout, stretch=10)

        ########## LEFT SIDE

        # Update Button
        self.update_btn: QtWidgets.QPushButton = QtWidgets.QPushButton("Update")
        self.update_btn.clicked.connect(lambda: self.UpdateData_Btn())
        self.left_main_layout.addWidget(self.update_btn)

        # Set Start EID Button
        self.set_startEID_btn: QtWidgets.QPushButton = QtWidgets.QPushButton("Set Start EID")
        self.set_startEID_btn.clicked.connect(lambda: self.SetStartEID_Btn())
        self.left_main_layout.addWidget(self.set_startEID_btn)

        # Set End EID Button
        self.set_endEID_btn: QtWidgets.QPushButton = QtWidgets.QPushButton("Set End EID")
        self.set_endEID_btn.clicked.connect(lambda: self.SetEndEID_Btn())
        self.left_main_layout.addWidget(self.set_endEID_btn)

        label_tmp = QtWidgets.QLabel('Start EID:')
        self.left_main_layout.addWidget(label_tmp)
        
        self.startEID: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.startEID.setValidator(QtGui.QIntValidator())
        self.startEID.setObjectName("Start EID")
        self.startEID.setText("0")
        self.left_main_layout.addWidget(self.startEID)

        label_tmp = QtWidgets.QLabel('End EID:')
        self.left_main_layout.addWidget(label_tmp)

        self.endEID: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.endEID.setValidator(QtGui.QIntValidator())
        self.endEID.setObjectName("End EID")
        self.endEID.setText("10000")
        self.left_main_layout.addWidget(self.endEID)

        self.uniques_meshes_checkbox = QtWidgets.QCheckBox("Unique Meshes")
        self.uniques_meshes_checkbox.setChecked(True)
        self.left_main_layout.addWidget(self.uniques_meshes_checkbox)
        self.uniques_textures_checkbox = QtWidgets.QCheckBox("Unique Textures")
        self.uniques_textures_checkbox.setChecked(True)
        self.left_main_layout.addWidget(self.uniques_textures_checkbox)

        ########## RIGHT SIDE

        ### Meshes
        self.meshes_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.right_main_layout.addLayout(self.meshes_layout)

        select_mesh_eid_btn: QtWidgets.QPushButton = QtWidgets.QPushButton("Select Mesh")
        select_mesh_eid_btn.clicked.connect(lambda: self.SelectMeshEID_Btn())
        self.meshes_layout.addWidget(select_mesh_eid_btn)

        self.meshes_list: QtWidgets.QListWidget = QtWidgets.QListWidget()
        self.meshes_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.meshes_list.setMinimumHeight(50)
        self.meshes_list.setMaximumWidth(300)
        self.meshes_layout.addWidget(self.meshes_list)

        ### Textures
        self.texures_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.right_main_layout.addLayout(self.texures_layout)

        select_texture_eid_btn: QtWidgets.QPushButton = QtWidgets.QPushButton("Select Texture")
        select_texture_eid_btn.clicked.connect(lambda: self.SelectTextureEID_Btn())
        self.texures_layout.addWidget(select_texture_eid_btn)

        self.textures_list: QtWidgets.QListWidget = QtWidgets.QListWidget()
        self.textures_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.textures_list.setMinimumHeight(50)
        self.textures_list.setMaximumWidth(300)
        self.texures_layout.addWidget(self.textures_list)

    def GetStartEID(self):
        return int(self.startEID.text())

    def GetEndEID(self):
        return int(self.endEID.text())

    def SelectMeshEID_Btn(self):
        global the_window
        if len(self.meshes_list.selectedIndexes()) > 0:
            cur_index = self.meshes_list.currentIndex().row()
            cur_data = the_window.main_data.meshes_data[cur_index]
            the_window.ctx.SetEventID([], the_window.ctx.CurEvent(), cur_data[0], False)
            the_window.ctx.ShowMeshPreview()

    def SelectTextureEID_Btn(self):
        global the_window
        if len(self.textures_list.selectedIndexes()) > 0:
            cur_index = self.textures_list.currentIndex().row()
            cur_data = the_window.main_data.textures_data[cur_index]
            event_id = cur_data[0]
            res: rd.ResourceDescription = the_window.ctx.GetResources()[cur_data[4]]
            the_window.ctx.SetEventID([], the_window.ctx.CurEvent(), event_id, False)
            the_window.ctx.GetTextureViewer().ViewTexture(res.resourceId, rd.CompType.UNormSRGB, True)

    def UpdateData_Btn(self):
        global the_window
        the_window.UpdateData()

    def SetStartEID_Btn(self):
        global the_window
        self.startEID.setText(str(the_window.ctx.CurEvent()))

    def SetEndEID_Btn(self):
        global the_window
        self.endEID.setText(str(the_window.ctx.CurEvent()))

    def ClearUI(self):
        self.meshes_list.clear()
        self.textures_list.clear()

    def UpdateUI(self):
        global the_window

        self.ClearUI()

        unique_res_ids: set = set()

        # Set Meshes
        for mesh_data in the_window.main_data.meshes_data:
            mesh_item: QtWidgets.QListWidgetItem = QtWidgets.QListWidgetItem()
            mesh_item.setText(str(mesh_data[1]))

            res_id = mesh_data[2]

            if res_id not in unique_res_ids:
                mesh_item.setTextColor(QtGui.QColor(150, 50, 0))
                unique_res_ids.add(res_id)

            self.meshes_list.addItem(mesh_item)

        unique_res_ids.clear()
        
        # Set Textures
        for tex_data in the_window.main_data.textures_data:
            tex_item: QtWidgets.QListWidgetItem = QtWidgets.QListWidgetItem()
            tex_item.setText(str(tex_data[1]) + " x " + str(tex_data[2]))

            res_id = tex_data[4]

            if res_id not in unique_res_ids:
                tex_item.setTextColor(QtGui.QColor(160, 80, 0))
                unique_res_ids.add(res_id)

            self.textures_list.addItem(tex_item)
