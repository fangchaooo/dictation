from pprint import pprint

from PyQt6.QtGui import QFont, QPalette, QColor
from dictation_db import DictationDB
from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex, QStringListModel, QAbstractListModel, QVariant, QPoint, \
    QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QListView, QMainWindow, QTreeView, QVBoxLayout, QWidget, QStyledItemDelegate, QApplication, \
    QStyle, QStyleOptionViewItem, QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QDialog

import dictation
import sys


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()

        mode_label = QLabel("Mode:")
        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(["Cycling Remember", "Dictation"])
        layout.addWidget(mode_label)
        layout.addWidget(self.mode_combobox)

        time_gap_label = QLabel("Playing Time Gap:")
        self.time_gap_spinbox = QSpinBox()
        self.time_gap_spinbox.setRange(1, 10)  # You can adjust the range as needed
        layout.addWidget(time_gap_label)
        layout.addWidget(self.time_gap_spinbox)

        speed_label = QLabel("Speed:")
        self.speed_spinbox = QDoubleSpinBox()
        self.speed_spinbox.setRange(1.0, 2.0)  # You can adjust the range as needed
        layout.addWidget(speed_label)
        layout.addWidget(self.speed_spinbox)

        self.setLayout(layout)

    def animate_from_bottom(self):
        # Get the position of the parent widget
        parent_pos = self.parentWidget().pos()

        # Calculate the starting and ending positions for the animation
        start_pos = QPoint(parent_pos.x(), parent_pos.y() + self.parentWidget().height())
        end_pos = parent_pos

        # Set the initial position of the dialog outside the widget's area
        self.move(start_pos)

        # Create a property animation to smoothly move the dialog
        animation = QPropertyAnimation(self, b'pos')
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setDuration(300)  # Animation duration in milliseconds
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)  # Easing curve for smooth animation

        # Start the animation
        animation.start()


class CustomItem:
    def __init__(self, text, parent=None):
        self.text = text
        self.children = []
        self.parent = parent


class CustomModel(QAbstractItemModel):
    def __init__(self, root_item):
        super().__init__()
        self.root_item = root_item

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.children[row]
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = None
        if child_item:
            parent_item = child_item.parent

        if parent_item == self.root_item:
            return QModelIndex()

        return self.createIndex(self.root_item.children.index(parent_item), 0, parent_item)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        return len(parent_item.children)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            return item.text

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        # if orientation == Qt.ItemDataRole.Horizontal and role == Qt.ItemDataRole.DisplayRole:
        return "Items"


class WordDictation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_dictations = None
        self.root_item = None
        self.tree_view = None
        self.model_recent_error_words = None
        self.model_all_words = None
        self.ui = None
        self.audio_words_all = []
        self.audio_recent_error_words = []
        self.dictations_words = []
        self.select_listview_name = None
        self.db = DictationDB()
        self.word_study_setting = SettingsDialog(self)

    def setup_ui(self, ui: dictation.Ui_Form):
        self.ui = ui
        self.tree_view = ui.treeViewAllDictationWord
        self.root_item = CustomItem("Root")
        model = CustomModel(self.root_item)
        self.tree_view.setModel(model)
        self.tree_view.clicked.connect(self.on_item_clicked)

        # two listview show all words and error words
        self.model_all_words = QStringListModel()
        self.model_recent_error_words = QStringListModel()
        self.model_all_words.setStringList(self.audio_words_all)
        self.model_recent_error_words.setStringList(self.audio_recent_error_words)
        self.ui.listViewAllWord.setModel(self.model_all_words)
        self.ui.listViewRecentErrorWord.setModel(self.model_recent_error_words)
        self.model_all_words.dataChanged.connect(self.all_words_label_changed)
        self.ui.listViewAllWord.clicked.connect(self.all_word_list_view_selected)
        self.ui.listViewRecentErrorWord.clicked.connect(self.recent_error_word_list_view_selected)
        self.model_recent_error_words.dataChanged.connect(self.recent_error_words_label_changed)
        self.init_word_treeview()

        ui.btnStartLearnWord.clicked.connect(self.click_start_learn_word)

    def click_start_learn_word(self):
        self.word_study_setting.animate_from_bottom()
        self.word_study_setting.exec()

    def init_word_treeview(self):
        self.audio_dictations = self.db.get_audio_and_wordinfo_for_tree_view()
        data_dict = {}
        items = []
        self.dictations_words = []
        for audio, dictation in self.audio_dictations:
            if audio.name not in data_dict:
                data_dict[audio.name] = CustomItem(audio.name, self.root_item)
                items.append(data_dict[audio.name])
                self.dictations_words.append({"audio": audio, "dictation": []})
            if dictation:
                dictation_text = f"{dictation.dictation_time.strftime('%Y/%m/%d %H:%M')}"
                data_dict[audio.name].children.append(CustomItem(dictation_text, data_dict[audio.name]))
                for w in self.dictations_words:
                    if w["audio"].name == dictation.audio_name:
                        w["dictation"].append(dictation)

        self.root_item.children = items
        self.tree_view.expandAll()
        self.tree_view.setHeaderHidden(True)

    def customize_label(self, label, color, font_size):
        font = QFont()
        font.setPointSize(font_size)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Text, QColor(color))

        label.setFont(font)
        label.setPalette(palette)

    def all_word_list_view_selected(self):
        self.select_listview_name = "all_word_list_view"
        self.ui.listViewAllWord.setStyleSheet("QListView { border: 2px solid red; }")
        self.ui.listViewRecentErrorWord.setStyleSheet("")  # Reset style sheet

    def recent_error_word_list_view_selected(self):
        self.select_listview_name = "recent_error_word_list_view"
        self.ui.listViewRecentErrorWord.setStyleSheet("QListView { border: 2px solid red; }")
        self.ui.listViewAllWord.setStyleSheet("")  # Reset style sheet

    def all_words_label_changed(self):
        print("change")
        self.ui.labelAllWord.setText(f"全部单词（{len(self.model_all_words)}）")

    def recent_error_words_label_changed(self):
        self.ui.labelRecentErrorWord.setText(f"近期错误（{len(self.model_recent_error_words)}）")

    def get_all_dictition_info(self):
        pass

    def on_item_clicked(self, index):
        item = index.internalPointer()
        index1 = None
        index2 = None
        if item:
            if index.parent().isValid():
                index2 = index.parent().row()
                print("Child Clicked. Index:", index.row(), "Parent Index:", index.parent().row())
            else:
                index1 = index.row()
                print("Parent Clicked. Index:", index.row())
        self.audio_words_all = [x.word for x in self.dictations_words[index1]["audio"].words]
        self.model_all_words.setStringList(self.audio_words_all)
