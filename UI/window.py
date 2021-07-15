# coding=ascii

"""
@!Brief
"""

from PySide2 import QtWidgets

from UI import utils


class Window(QtWidgets.QMainWindow):

    """
    @!Brief
    """

    def __init__(self, window_title):
        super(Window, self).__init__()

        self.setWindowTitle(window_title)
        self.master_widget = QtWidgets.QWidget()
        self.master_layout = utils.base_layout(self.master_widget, spacing=5)
        self.setCentralWidget(self.master_widget)
