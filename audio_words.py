from PyQt6.QtWidgets import QMainWindow, QMenu, QListView
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QIcon, QStandardItemModel, QColor, QBrush
from PyQt6.QtCore import Qt, QAbstractListModel, pyqtSignal, QByteArray, QMimeData
import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, pyqtSignal
import dictation


class CustomListModel(QAbstractListModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.list_data = data
        self.clicked_index = None

    def rowCount(self, parent=QModelIndex()):
        return len(self.list_data)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.list_data[index.row()])
        elif role == Qt.ItemDataRole.BackgroundRole and index == self.clicked_index:
            return QBrush(QColor(0, 255, 0))  # Set background color for clicked item
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            self.list_data[index.row()] = value
            self.dataChanged.emit(index, index)  # Emit signal to update view
            return True
        return False

    def removeRow(self, row, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        del self.list_data[row]
        self.endRemoveRows()
        return True

    def all_data(self):
        return self.list_data


class AudioWordList(QMainWindow):
    signalListViewItem = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = None
        self.list_view = None
        self.model = None

    def setup_ui(self, ui: dictation.Ui_Form):
        self.ui = ui
        self.list_view = self.ui.WordTimelistView
        self.list_view.clicked.connect(self.itemClicked)  # Connect clicked signal to slot
        self.list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.showContextMenu)

        self.list_view.setDragEnabled(True)
        self.list_view.setAcceptDrops(True)
        self.list_view.setDropIndicatorShown(True)
        self.list_view.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.list_view.setSelectionMode(QListView.SelectionMode.SingleSelection)

    def all_data(self):
        return self.list_view.model().all_data()

    def showContextMenu(self, pos):
        index = self.list_view.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            insert_action = menu.addAction("Insert Item After")
            delete_action = menu.addAction("Delete Item")
            action = menu.exec(self.mapToGlobal(pos))
            if action == insert_action:
                self.insertAfterSelectedItem(index.row() + 1, "")
            elif action == delete_action:
                self.deleteItem(index.row())

    def updateListView(self, data):
        self.model = CustomListModel(data)
        self.list_view.setModel(self.model)

    def itemClicked(self, index):
        for index_ in self.list_view.selectedIndexes():
            item = self.list_view.model().data(index_, Qt.ItemDataRole.DisplayRole)
            print(f"click {index_.row()} item {item}")
            self.signalListViewItem.emit(item)

    def dropEvent(self, event):
        if event.source() == self.list_view:
            super().dropEvent(event)
            event.accept()

    def editTextChanged(self, word_time_list):
        word, start, end = word_time_list
        save_str = f"{word} [{start}, {end}]"
        selected_index = self.list_view.selectionModel().currentIndex()
        if selected_index.isValid():
            self.list_view.model().setData(selected_index, save_str, Qt.ItemDataRole.EditRole)

    def insertAfterSelectedItem(self, new_item_text):
        selected_index = self.list_view.selectionModel().currentIndex()
        if selected_index.isValid():
            row = selected_index.row()
            if new_item_text:
                self.list_view.model().insertRow(row + 1, new_item_text)

    def removeSelectedItem(self):
        selected_index = self.list_view.selectionModel().currentIndex()
        if selected_index.isValid():
            row = selected_index.row()
            self.list_view.model().removeRow(row)

    def deleteItem(self, row):
        self.list_view.model().removeRow(row)

    def get_all_data(self):
        all_data = self.list_view.model().data()
