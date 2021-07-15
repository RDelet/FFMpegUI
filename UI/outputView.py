# coding=ascii

"""
@!Brief
"""

import os

from PySide2 import QtCore, QtGui, QtWidgets

from UI import utils
from Helpers import data, path, ffmpeg
from Helpers.log import log


class OutputView(QtWidgets.QTabWidget):

    def __init__(self, view, parent=None):
        super(OutputView, self).__init__(parent)

        self.view = view
        self.ffmpeg_utils = ffmpeg.FFMPEG("CONVERTER UI")

        master_layout = QtWidgets.QVBoxLayout()
        master_layout.setContentsMargins(5, 5, 5, 5)
        master_layout.setSpacing(5)
        self.setLayout(master_layout)

        #    Video
        video_widget = QtWidgets.QWidget(self)
        video_layout = QtWidgets.QVBoxLayout()
        video_layout.setContentsMargins(5, 5, 5, 5)
        video_layout.setSpacing(5)
        master_layout.addLayout(video_layout)
        self.addTab(video_widget, "Video")

        #   Input path
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.setContentsMargins(5, 15, 5, 5)
        input_layout.setSpacing(5)
        video_layout.addLayout(input_layout)

        input_text = QtWidgets.QLabel("Input path: ", self)
        input_text.setFixedSize(100, 20)
        input_layout.addWidget(input_text)

        self.qt_input_path = QtWidgets.QLabel("", self)
        self.qt_input_path.setFixedHeight(20)
        self.qt_input_path.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain)
        input_layout.addWidget(self.qt_input_path)

        #   Output path
        output_layout = QtWidgets.QHBoxLayout()
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_layout.setSpacing(5)
        video_layout.addLayout(output_layout)
        qt_output_text = QtWidgets.QLabel("Output path: ", self)
        qt_output_text.setFixedSize(100, 20)
        self.qt_output_path = QtWidgets.QLineEdit(self)
        self.qt_output_path.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.qt_output_path.setFixedHeight(20)
        self.qt_output_path.editingFinished.connect(self.__output_directory_changed)
        output_layout.addWidget(qt_output_text)
        output_layout.addWidget(self.qt_output_path)

        s_directory_icon = os.path.join(path.ICON, "directory.png")
        directory_button = utils.icon_button(output_layout, 20, s_directory_icon)
        directory_button.clicked.connect(self.__directory_clicked)

        #   File name
        name_layout = QtWidgets.QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(5)
        video_layout.addLayout(name_layout)
        qt_output_text = QtWidgets.QLabel("File Name: ", self)
        qt_output_text.setFixedSize(100, 20)
        self.qt_file_name = QtWidgets.QLineEdit(self)
        self.qt_file_name.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.qt_file_name.setFixedHeight(20)
        self.qt_file_name.editingFinished.connect(self.__edit_file_name)
        name_layout.addWidget(qt_output_text)
        name_layout.addWidget(self.qt_file_name)

        # FFMpeg
        a_containers = self.ffmpeg_utils.video_containers()
        a_encoders = self.ffmpeg_utils.get_video_codecs()
        a_presets = self.ffmpeg_utils.video_preset()
        self.qt_formats, self.qt_codecs, self.qt_preset = utils.combo_box(
            video_layout, ["Formats", "Codecs", "Preset"], [a_containers, [x for x in a_encoders.keys()], a_presets],
            ([100, 0, 20], ) * 3, spacing=3
        )
        self.qt_preset.setCurrentIndex(a_presets.index("medium"))

        #   Video size
        size_layout = QtWidgets.QHBoxLayout()
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.setSpacing(5)
        video_layout.addLayout(size_layout)
        qt_output_text = QtWidgets.QLabel("Video Size: ", self)
        qt_output_text.setFixedSize(100, 20)
        self.qt_change_size = QtWidgets.QCheckBox(self)
        self.qt_change_size.stateChanged.connect(self.__video_size_checked)
        self.qt_size_width = QtWidgets.QLineEdit("1280", self)
        self.qt_size_width.setValidator(QtGui.QDoubleValidator())
        self.qt_size_width.setDisabled(True)
        self.qt_size_height = QtWidgets.QLineEdit("720", self)
        self.qt_size_height.setValidator(QtGui.QDoubleValidator())
        self.qt_size_height.setDisabled(True)
        size_layout.addWidget(qt_output_text)
        size_layout.addWidget(self.qt_change_size)
        size_layout.addWidget(self.qt_size_width)
        size_layout.addWidget(self.qt_size_height)

        #   Video CRF
        crf_layout = QtWidgets.QHBoxLayout()
        crf_layout.setContentsMargins(0, 0, 0, 0)
        crf_layout.setSpacing(5)
        video_layout.addLayout(crf_layout)
        qt_output_text = QtWidgets.QLabel("CRF: ")
        qt_output_text.setFixedSize(100, 20)
        self.qt_crf_value = QtWidgets.QLineEdit(self)
        self.qt_crf_value.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.qt_crf_value.setFixedHeight(20)
        self.qt_crf_value.setValidator(QtGui.QIntValidator(0, 100))
        crf_layout.addWidget(qt_output_text)
        crf_layout.addWidget(self.qt_crf_value)

        video_layout.addStretch()

    def set_from_data(self, d):
        self.qt_input_path.setText(d.file_path)
        self.qt_output_path.setText(d.output_dir)
        self.qt_file_name.setText(d.full_name)
        self.qt_crf_value.setText(str(d.crf))

        i_index = self.qt_formats.findText(d.output_extension)
        if i_index:
            self.qt_formats.setCurrentIndex(i_index)

        i_index = self.qt_codecs.findText(d.video_codec)
        if i_index:
            self.qt_codecs.setCurrentIndex(i_index)

    def __selected(self):
        return self.view.selectedIndexes()

    @staticmethod
    def __data_from_index(qt_index):
        return qt_index.data(data.DATA_ROLE)

    def __directory_clicked(self):
        """
        !@Brief Action when directory_button clicked
        """
        s = utils.directory_chooser(self)
        if s:
            self.qt_output_path.setText(s)
            self.__output_directory_changed(s)

    def __output_directory_changed(self, s=None):
        a = self.__selected()
        if not a:
            return
        d = self.__data_from_index(a[0])
        d.output_dir = s if s else self.qt_output_path.text()
        log.debug('Output directory change to {0}'.format(s))

    def __video_size_checked(self, v):
        self.qt_size_width.setDisabled(not v)
        self.qt_size_height.setDisabled(not v)
        log.debug('Change video size change to {0}'.format(v))

    def __edit_file_name(self):
        s = self.qt_file_name.text().split('.')[0]
        a = self.__selected()
        if not a:
            return
        d = self.__data_from_index(a[0])
        d.name = s
        self.qt_file_name.setText('{0}.{1}'.format(d.name, d.extension))
        log.debug('File name change to {0}.'.format(d.name))
