# coding=ascii

"""
@!Bief
"""

from PySide2 import QtWidgets

from UI.treeView import TreeView


class InputView(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super(InputView, self).__init__(parent)

        self.setParent(parent)

        master_layout = QtWidgets.QVBoxLayout()
        master_layout.setContentsMargins(5, 5, 5, 5)
        master_layout.setSpacing(5)
        self.setLayout(master_layout)

        self.view = TreeView(None, editable=False)
        master_layout.addWidget(self.view)
        self.addTab(self.view, "Sources")
