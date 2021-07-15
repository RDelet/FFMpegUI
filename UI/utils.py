# coding=ascii

"""
@!Brief
"""

import os

from PySide2 import QtWidgets, QtCore, QtGui

from Helpers import path


def directory_chooser(qt_parent, b_options=None):
    """
    !@Brief Get directory path with PySide dialog window.

    @type qt_parent: QtWidgets.QObject
    @parem qt_parent: PySide object.
    @type b_options: QtWidgets.QFileDialog.*
    @param b_options: QFileDialog options.

    @rtype: string
    @return: Directory path.
    """
    if b_options is None:
        b_options = QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly
    s_directory = QtWidgets.QFileDialog.getExistingDirectory(qt_parent, '', '', b_options)

    return s_directory if s_directory else None


def set_size(ui_object, height, width):
    if height > 0:
        ui_object.setFixedHeight(height)
    if width > 0:
        ui_object.setFixedWidth(width)


def base_layout(parent=None, vector='V', margin=(0, 0, 0, 0), spacing=0):

    qt_base_layout = None

    if vector == 'H':
        qt_base_layout = QtWidgets.QHBoxLayout()
    elif vector == 'V':
        qt_base_layout = QtWidgets.QVBoxLayout()

    qt_base_layout.setContentsMargins(margin[0], margin[1], margin[2], margin[3])
    qt_base_layout.setSpacing(spacing)

    if parent is not None:
        if isinstance(parent, QtWidgets.QWidget):
            parent.setLayout(qt_base_layout)
        else:
            parent.addLayout(qt_base_layout)

    return qt_base_layout


def icon_button(parent=None, icon_size=20, icon_picture='directory.png'):

    #   Icon
    qt_pixmap = QtGui.QPixmap(os.path.join(path.ICON, icon_picture))
    qt_icon = QtGui.QIcon(qt_pixmap)

    #   Button
    qt_button = QtWidgets.QPushButton()
    qt_button.setFixedSize(icon_size, icon_size)
    qt_button.setIcon(qt_icon)
    qt_button.setIconSize(QtCore.QSize(icon_size, icon_size))
    qt_button.setFlat(True)

    if parent is not None:
        parent.addWidget(qt_button)

    return qt_button


def button(parent, labels, size, margin=(0, 0, 0, 0), spacing=0, vector='V', flat=False, **kwargs):

    #    Variables
    a_color = kwargs.get("color", None)
    i_icon_size = kwargs.get("icon_size", 20)
    a_icon_path = kwargs.get("icon_path", list())
    a_tool_tip = kwargs.get("tool_tip", list())

    all_qt_button = []
    master_layout = base_layout(parent, vector, margin, spacing)

    for i, (l, s) in enumerate(zip(labels, size)):

        qt_button = QtWidgets.QPushButton()
        qt_button.setText(l)
        qt_button.setFlat(flat)
        set_size(qt_button, s[1], s[0])
        master_layout.addWidget(qt_button)

        if a_icon_path:
            qt_pixam = QtGui.QPixmap(a_icon_path[i])
            qt_icon = QtGui.QIcon(qt_pixam)
            qt_button.setIcon(qt_icon)
            qt_button.setIconSize(QtCore.QSize(i_icon_size, i_icon_size))

        if a_tool_tip:
            qt_button.setToolTip(a_tool_tip[i])

        if a_color is not None:
            r = a_color[i][0]
            g = a_color[i][1]
            b = a_color[i][2]
            qt_button.setStyleSheet('background-color: rgb(%s, %s, %s)' % (r, g, b))

        all_qt_button.append(qt_button)

    return all_qt_button


def combo_box(parent, labels, items, size, margin=(0, 0, 0, 0), spacing=0, vector='V', **kwargs):

    all_combobox = []
    all_qt_button = []

    b_button_label = kwargs.get('buttonLabel', False)
    s_icon_path = kwargs.get('buttonIcon', 'import.png')
    i_icon_size = kwargs.get('iconsSize', 20)

    master_layout = base_layout(parent, vector, margin, spacing)

    for t, s, item in zip(labels, size, items):

        combobox_layout = base_layout(vector='H')
        master_layout.addLayout(combobox_layout)

        #    Label
        label = QtWidgets.QLabel(None)
        label.setText(t)
        label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        combobox_layout.addWidget(label)
        set_size(label, s[2], s[0])

        #    ComboBox
        combobox = QtWidgets.QComboBox(None)
        combobox_layout.addWidget(combobox)
        all_combobox.append(combobox)
        set_size(combobox, s[2], s[1])

        if item:
            combobox.addItems(item)

        #   Button
        if b_button_label is True:
            qt_button = icon_button(combobox_layout, i_icon_size, s_icon_path)
            all_qt_button.append(qt_button)

    if b_button_label is False:
        return all_combobox
    else:
        return all_combobox, all_qt_button
