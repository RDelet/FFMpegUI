# coding=ascii

"""
@!Brief
"""

from PySide2 import QtWidgets, QtCore, QtGui


class TreeView(QtWidgets.QTreeView):
    index_changed = QtCore.Signal(QtCore.QItemSelection, QtCore.QItemSelection)
    TYPE_ROLE = QtCore.Qt.UserRole
    DATA_ROLE = QtCore.Qt.UserRole + 1

    def __init__(self, parent, **kwargs):
        super(TreeView, self).__init__(parent)

        self._model = QtGui.QStandardItemModel(self)
        self.setModel(self._model)
        self.setHeaderHidden(kwargs.get("header_hidden", True))
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setWindowTitle(kwargs.get("title", ''))

        width = kwargs.get("width", None)
        if width:
            self.setFixedWidth(width)
        height = kwargs.get("height", None)
        if height:
            self.setFixedHeight(height)

    def model(self):
        return self._model

    def clear_content(self):
        """
        !@Brief
        """
        row_count = self._model.rowCount()
        parent_item = self._model.invisibleRootItem()
        parent_item.removeRows(0, row_count)

    def selectionChanged(self, selected, deselected):
        super(TreeView, self).selectionChanged(selected, deselected)
        self.index_changed.emit(selected, deselected)

    def item_from_index(self, qt_index):

        """
        !@Brief Get item from index

        @type qt_index: PySide2.QtCore.QModelIndex
        @param qt_index: TreeView index for get item.

        @return: Item from given index
        """

        parent_item = self.get_parent_item(qt_index)
        qt_item = parent_item.child(qt_index.row(), qt_index.column())

        return qt_item

    def get_parent_item(self, qt_index=None):

        """
        !@Brief Get Parent item of QModelIndex

        @type qt_index: PySide2.QtCore.QModelIndex
        @param qt_index: Index you want to get parent item

        @rtype: PySide2.QtGui.QStandardItem
        @return: Parent item of model index
        """

        qt_parent_item = self._model.invisibleRootItem()
        if qt_index:
            parent_index = qt_index.parent()
            if not parent_index.isValid():
                return qt_parent_item

            if isinstance(parent_index.model(), QtCore.QAbstractProxyModel):
                parent_index = self.filter().mapToSource(parent_index)
            item_parent = self._model.itemFromIndex(parent_index)
            if item_parent:
                qt_parent_item = item_parent

        return qt_parent_item
