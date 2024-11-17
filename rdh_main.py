import renderdoc as rd
import qrenderdoc as qrd

import PySide2
from PySide2 import QtCore, QtWidgets, QtGui


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
        self.update_btn.clicked.connect(lambda: self.UpdateData())
        self.left_main_layout.addWidget(self.update_btn)

        label_tmp = QtWidgets.QLabel('Start EID:')
        self.left_main_layout.addWidget(label_tmp)
        
        self.startEID: QtWidgets.QSpinBox = QtWidgets.QLineEdit()
        self.startEID.setValidator(QtGui.QIntValidator())
        self.startEID.setObjectName("Start EID")
        self.startEID.setText("0")
        self.left_main_layout.addWidget(self.startEID)

        label_tmp = QtWidgets.QLabel('End EID:')
        self.left_main_layout.addWidget(label_tmp)

        self.endEID: QtWidgets.QSpinBox = QtWidgets.QLineEdit()
        self.endEID.setValidator(QtGui.QIntValidator())
        self.endEID.setObjectName("End EID")
        self.endEID.setText("5000")
        self.left_main_layout.addWidget(self.endEID)

        ########## RIGHT SIDE

        ### Textures
        self.drawcalls_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.right_main_layout.addLayout(self.drawcalls_layout)

        select_drawcall_eid_btn: QtWidgets.QPushButton = QtWidgets.QPushButton("Select Drawcall")
        select_drawcall_eid_btn.clicked.connect(lambda: self.SelectDrawcallEIDButton())
        self.drawcalls_layout.addWidget(select_drawcall_eid_btn)

        self.drawcalls_list: QtWidgets.QListWidget = QtWidgets.QListWidget()
        self.drawcalls_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.drawcalls_list.setMinimumHeight(50)
        self.drawcalls_list.setMaximumWidth(300)
        self.drawcalls_layout.addWidget(self.drawcalls_list)

        ### Meshes
        self.meshes_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.right_main_layout.addLayout(self.meshes_layout)

        select_mesh_eid_btn: QtWidgets.QPushButton = QtWidgets.QPushButton("Select Mesh")
        select_mesh_eid_btn.clicked.connect(lambda: self.SelectMeshEIDButton())
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
        select_texture_eid_btn.clicked.connect(lambda: self.SelectTextureEIDButton())
        self.texures_layout.addWidget(select_texture_eid_btn)

        self.textures_list: QtWidgets.QListWidget = QtWidgets.QListWidget()
        self.textures_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.textures_list.setMinimumHeight(50)
        self.textures_list.setMaximumWidth(300)
        self.texures_layout.addWidget(self.textures_list)


    def SelectMeshEIDButton(self):
        pass


    def SelectTextureEIDButton(self):
        pass


    def SelectDrawcallEIDButton(self):
        pass


    def UpdateData(self):
        pass


class RDHWindow(qrd.CaptureViewer):
    def __init__(self, ctx: qrd.CaptureContext, version: str):
        super().__init__()

        self.ctx: qrd.CaptureContext = ctx
        self.version: str = version
        
        self.main_widget: MainWidget = MainWidget()

        ########## FINAL THINGS
        ctx.AddDockWindow(self.main_widget, qrd.DockReference.MainToolArea, None)
        ctx.AddCaptureViewer(self)


    def OnCaptureLoaded(self):
        pass


    def OnCaptureClosed(self):
        pass


    def OnSelectedEventChanged(self, event):
        pass


    def OnEventChanged(self, event):
        pass


class MainData():
    def __init__(self) -> None:
        self.drawcalls_data: list = []
        self.meshes_data: list = []
        self.textures_data: list = []
