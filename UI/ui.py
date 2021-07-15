# coding=ascii

"""
@!Brief
"""

import logging
import os
import sys
import traceback

from PySide2 import QtGui, QtCore, QtWidgets

from Helpers.color import Color
from Helpers.log import log, Handler
from Helpers.threading import Thread
from Helpers import path, data
from UI import inputView, outputView, utils
from UI.window import Window


class UI(Window):

    def __init__(self, window_title):
        super(UI, self).__init__(window_title)

        self._to_process = list()
        self._is_active = False
        self._current_item = None
        self._current_thread = None

        # =========================================================
        #   Base widget

        self.v_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, self)
        self.v_splitter.setHandleWidth(5)
        self.v_splitter.setChildrenCollapsible(True)
        self.master_layout.addWidget(self.v_splitter)

        convertor_widget = QtWidgets.QWidget(self.v_splitter)
        convertor_layout = QtWidgets.QVBoxLayout()
        convertor_layout.setContentsMargins(5, 5, 5, 5)
        convertor_layout.setSpacing(5)
        convertor_widget.setLayout(convertor_layout)

        verbose_widget = QtWidgets.QWidget(self.v_splitter)
        verbose_layout = QtWidgets.QVBoxLayout()
        verbose_layout.setContentsMargins(5, 5, 5, 5)
        verbose_layout.setSpacing(5)
        verbose_widget.setLayout(verbose_layout)

        # =========================================================
        #   Directory path

        directory_layout = QtWidgets.QHBoxLayout()
        directory_layout.setContentsMargins(0, 0, 0, 0)
        directory_layout.setSpacing(5)
        convertor_layout.addLayout(directory_layout)

        directory_label = QtWidgets.QLabel(self)
        directory_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        directory_label.setText("Directory Path")
        directory_layout.addWidget(directory_label)

        self._directory_text_field = QtWidgets.QLineEdit('', self)
        self._directory_text_field.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        directory_layout.addWidget(self._directory_text_field)
        self._directory_text_field.setFixedHeight(20)
        self._directory_text_field.textChanged.connect(self.__on_directory_path_changed)
        s_directory_icon = os.path.join(path.ICON, "directory.png")
        directory_button = utils.icon_button(directory_layout, 20, s_directory_icon)
        directory_button.clicked.connect(self.__on_directory_clicked)

        # =========================================================
        #   List input / output

        self.h_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)
        self.h_splitter.setHandleWidth(5)
        self.h_splitter.setChildrenCollapsible(True)
        convertor_layout.addWidget(self.h_splitter)

        self.input_view = inputView.InputView(self.h_splitter)
        self.input_view.view.index_changed.connect(self.__on_selection_changed)

        self.output_view = outputView.OutputView(self.input_view.view, parent=self.h_splitter)

        # =========================================================
        #   Export

        actions = [self.__on_convert_clicked, self.__on_stop_clicked]
        labels = ["Convert Selected", "Stop Selected"]
        sizes = ([0, 30], ) * len(labels)
        self.convert_button = utils.button(convertor_layout, labels, sizes, vector="H")

        for action, button in zip(actions, self.convert_button):
            button.clicked.connect(action)

        #   Verbose
        self._qt_verbose = QtWidgets.QTextEdit(self)
        verbose_layout.addWidget(self._qt_verbose)

        self._directory_text_field.setText(r'D:\RDE\Videos')

        Handler.connect(self.__print)
        log.debug('Hodor')

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "{0}".format(self.__class__.__name__)

    def kill_thread(self):
        try:
            self._current_thread.exit()
            self._current_thread.quit()
            self.reset()
        except Exception as e:
            log.error(traceback.format_exc(e))

    def next(self):
        if self._to_process:
            self.__process()

    @staticmethod
    def remove_converted(d):
        try:
            if os.path.exists(d.output_dir):
                os.remove(d.output_dir)
        except Exception as e:
            log.error(traceback.format_exc(e))

    def reset(self, item=None):
        if item and item in self._to_process:
            del self._to_process[self._to_process.index(item)]
        self._is_active = False
        self._current_item = None
        self._current_thread = None

    def __on_selection_changed(self):

        """
        !@Brief On Selection changed update output view.
        """

        a_selected_index = self.input_view.view.selectedIndexes()
        if not a_selected_index:
            return
        self.output_view.set_from_data(a_selected_index[0].data(data.DATA_ROLE))

    def __on_directory_clicked(self):
        """
        !@Brief Action when directory_button clicked
        """
        self._directory_text_field.setText(utils.directory_chooser(self))

    def __on_directory_path_changed(self):
        """
        !@Brief Action when text label changed.
        """
        d_path = self._directory_text_field.text()
        if not os.path.exists(d_path) or not os.path.isdir(d_path):
            return
        self.input_view.view.clear_content()
        for input_path in path.get_files(d_path):
            self.input_view.view.model().appendRow(self.__new_item(input_path))

    def __new_item(self, s_file_path):
        """!@Brief Create PySide QStandartItem from file path.

        @type s_file_path: string
        @param s_file_path: Path of file

        @rtype: QtGui.QStandartItem
        @return: PySide Item.
        """
        d = data.Item(s_file_path)
        icon = QtGui.QIcon(QtGui.QPixmap(os.path.join(path.ICON, "video_file.png")))
        qt_file_item = QtGui.QStandardItem(icon, '{0}.{1}'.format(d.name, d.extension))
        qt_file_item.setEditable(False)
        qt_file_item.setSelectable(True)
        qt_file_item.setSizeHint(QtCore.QSize(20, 20))
        qt_file_item.setData(d, data.DATA_ROLE)

        return qt_file_item

    def __on_convert_clicked(self):

        """
        !@Brief Convert file from ui datas.
        """

        a_selected_indexes = self.input_view.view.selectedIndexes()
        if not a_selected_indexes:
            log.error("No item selected !")
            return

        for qt_index in a_selected_indexes:
            if qt_index not in self._to_process:
                self._set_color(qt_index, Color.kGrey)
                self._to_process.append(qt_index)

        if not self._is_active:
            self.__process()

    def __on_stop_clicked(self):

        """
        !@Brief Stop convertion and delete output files.
        """

        a_selected_indexes = self.input_view.view.selectedIndexes()
        if not a_selected_indexes:
            log.error("No item selected !")
            return

        for qt_index in a_selected_indexes:
            if qt_index == self._current_item:
                self.kill_thread()
                self.remove_converted(qt_index.data(data.DATA_ROLE))
                self.reset(qt_index)
            if qt_index in self._to_process:
                del self._to_process[self._to_process.index(qt_index)]
            self._set_color(qt_index, Color.kGrey)

        self.__process()

    def __on_thread_finished(self):

        """
        !@Brief On current thread is finish remove current item to "to_process" list and reset variables.
        """
        self._set_color(self._current_item, Color.kGreen)
        self.reset()
        self.next()

    @staticmethod
    def __on_log(s, t):
        {logging.DEBUG: log.debug, logging.INFO: log.info, logging.WARNING: log.warning, logging.ERROR: log.error}[t](s)

    def __print(self, s_text):
        """!@Brief UI Verbose.

        @type s_text: string
        @param s_text: Particular verbose.
        """
        a_verbose_split = s_text.split("\n")
        if len(a_verbose_split) > 100:
            s_text = "\n".join(a_verbose_split[-100:])
        self._qt_verbose.setText('{0}\n{1}'.format(self._qt_verbose.toPlainText(), s_text))
        self._qt_verbose.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

    def __process(self):

        """
        !@Brief Process all items is "to_process" list.
        """

        if self._is_active or not self._to_process:
            return

        #   Get datas
        self._current_item = self._to_process[0]
        d = self._current_item.data(data.DATA_ROLE)
        d.is_processed = True
        self._set_color(self._current_item, Color.kOrange)

        #   Get thread
        try:
            self._current_thread = Thread(d, parent=self)
            self._current_thread.finished.connect(self.__on_thread_finished)
            self._current_thread.log.connect(self.__on_log)
            self._current_thread.start()
            self._is_active = True
        except Exception as e:
            log.error(traceback.format_exc(e))
            self.kill_thread()
            self.remove_converted(d)
            self.reset(self._current_item)

    def _set_color(self, qt_index, item_color):

        """
        !@Brief Set color of item

        @type: QtCore.QModelIndex
        @param: Indec for change background
        @type item_color: Color
        @param item_color: Color datas
        """

        qt_item = self.input_view.view.item_from_index(qt_index)
        if qt_item:
            qt_color = QtGui.QBrush(QtGui.QColor(item_color[0], item_color[1], item_color[2], item_color[3]))
            qt_item.setBackground(qt_color)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ffmpeg_ui = UI("FFMpeg UI")
    ffmpeg_ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
