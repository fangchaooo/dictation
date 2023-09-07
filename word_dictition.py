from pprint import pprint

from PyQt6.QtGui import QFont, QPalette, QColor

from audio_player import AudioPlayerApp
from dictation_db import DictationDB
from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex, QStringListModel, QAbstractListModel, QVariant, QPoint, \
    QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QListView, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStyledItemDelegate, \
    QApplication, \
    QStyle, QStyleOptionViewItem, QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QDialog

import dictation
import sys


class WordLearningSetting:
    def __init__(self):
        self.played_times = None
        self.selected_mode = None
        self.time_gap = None
        self.speed = None


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setting = WordLearningSetting()

        self.setWindowTitle("Settings")

        layout = QVBoxLayout()

        # Mode ComboBox
        mode_label = QLabel("Mode:")
        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(["Cycling Remember", "Dictation"])
        layout.addWidget(mode_label)
        layout.addWidget(self.mode_combobox)

        # Playing Time Gap SpinBox
        time_gap_label = QLabel("Playing Time Gap:")
        self.time_gap_spinbox = QSpinBox()
        self.time_gap_spinbox.setRange(1, 10)  # You can adjust the range as needed
        layout.addWidget(time_gap_label)
        layout.addWidget(self.time_gap_spinbox)

        # Speed DoubleSpinBox
        speed_label = QLabel("Speed:")
        self.speed_spinbox = QDoubleSpinBox()
        self.speed_spinbox.setRange(1.0, 2.0)  # You can adjust the range as needed
        layout.addWidget(speed_label)
        layout.addWidget(self.speed_spinbox)

        # Played Times SpinBox
        played_times_label = QLabel("Played Times:")
        self.played_times_spinbox = QSpinBox()
        self.played_times_spinbox.setRange(1, 10)  # Adjust the range as needed
        layout.addWidget(played_times_label)
        layout.addWidget(self.played_times_spinbox)

        # Add a Save button
        self.save_button = QPushButton("Save")
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        if parent:
            parent_center = parent.geometry().center()
            self.move(parent_center - self.rect().center())

    def save_settings(self):
        self.setting.selected_mode = self.mode_combobox.currentText()
        self.setting.time_gap = self.time_gap_spinbox.value()
        self.setting.speed = self.speed_spinbox.value()
        self.setting.played_times = self.played_times_spinbox.value()


class CyclingRemember(QMainWindow):
    def __init__(self, player: AudioPlayerApp, parent=None):
        super().__init__(parent)
        self.ui = None
        self.words_data = None
        self.player = player
        self.setting = None
        self.words_intervals = None

    def setup_ui(self, ui: dictation.Ui_Form):
        ui.btnWordPlaySetting.clicked.connect(self.start_setting)
        ui.btnWordPlayNext.clicked.connect(self.next)
        ui.btnWordPlayPrev.clicked.connect(self.prev)
        ui.btnWordPlayStop.clicked.connect(self.prev)

        style = """
                QProgressBar {
                    border: 2px solid #aaa;
                    border-radius: 5px;
                    background: #f1f1f1;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background: #4CAF50;
                    width: 20px;
                }
                """
        ui.progressBarWordPlay.setStyleSheet(style)
        self.ui = ui

    def update_text(self, line1, line2):
        html = f"""
            <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
            <html>
            <head>
                <meta name="qrichtext" content="1" />
                <style type="text/css">
                    p, li {{ white-space: pre-wrap; }}
                </style>
            </head>
            <body style="font-family: Arial, sans-serif; font-size: 14pt; font-weight: 400; font-style: normal; text-align: center;">
                <p style="margin: 0;">
                    <span style="font-size: 36pt; font-weight: 600; color: #333;">{line1}</span>
                </p>
                <p style="margin: 12px 0;">
                    <span style="font-size: 24pt; color: #666; vertical-align: super;">{line2}</span>
                </p>
            </body>
            </html>
            """
        self.ui.textEditWordDisplay.setHtml(html)

    def set_words_data(self, data):
        self.words_data = data

    def set_play_setting(self, setting):
        self.setting = setting

    def start_setting(self):
        pass

    def play(self):
        self.ui.progressBarWordPlay.setRange(0, len(self.words_data.words))
        audio_path = self.words_data.location
        self.player.signalIntervalIndex.connect(self.display_word)
        if self.player.paly_source != audio_path:
            self.player.open_music(False, audio_path)
            self.player.set_volume(100)
        words = self.words_data.words
        words_intervals = [[word.word_start_time, word.word_end_time] for word in words]
        self.player.start_play_interval(words_intervals, self.setting.time_gap, self.setting.speed,
                                        self.setting.played_times)

    def pause(self):
        self.player.pause_interval()

    def next(self):
        self.player.next_interval()

    def prev(self):
        self.player.prev_interval()

    def display_word(self, index):
        if self.words_data:
            word, mean = self.words_data.words[index].word, self.words_data.words[index].word_chinese_mean
            print(word, mean)
            self.update_text(word, mean)
            self.ui.progressBarWordPlay.setValue(index)
            self.ui.progressBarWordPlay.setFormat(f"Processing: {index}/{len(self.words_data.words)}")


class InputDictation(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.ui = None

    def setup_ui(self, ui: dictation.Ui_Form):
        self.ui = ui


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
    def __init__(self, player):
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

        self.player = player
        self.tree_view_select_parent_index = None
        self.tree_view_select_children_index = None
        self.cycling_remember = CyclingRemember(player)

    def setup_ui(self, ui: dictation.Ui_Form):
        self.cycling_remember.setup_ui(ui)
        self.ui = ui
        self.tree_view = ui.treeViewAllDictationWord
        self.root_item = CustomItem("Root")
        model = CustomModel(self.root_item)
        self.tree_view.setModel(model)
        self.tree_view.clicked.connect(self.on_treeview_item_clicked)

        # two listview show all words and error words
        self.model_all_words = QStringListModel()
        self.model_recent_error_words = QStringListModel()
        self.model_all_words.setStringList(self.audio_words_all)
        self.model_recent_error_words.setStringList(self.audio_recent_error_words)
        self.ui.listViewAllWord.setModel(self.model_all_words)
        self.ui.listViewRecentErrorWord.setModel(self.model_recent_error_words)
        self.model_all_words.dataChanged.connect(self.all_words_label_changed)
        self.model_recent_error_words.dataChanged.connect(self.recent_error_words_label_changed)

        self.init_word_treeview()

        ###################### 选择学习模式 #########################
        # 单词组选择
        self.ui.listViewAllWord.clicked.connect(self.all_word_list_view_selected)
        self.ui.listViewRecentErrorWord.clicked.connect(self.recent_error_word_list_view_selected)
        # 开始学习
        self.ui.btnStartLearnWord.clicked.connect(self.click_start_learn_word)
        # 保存选项, 打开相应学习页面
        self.word_study_setting.save_button.clicked.connect(self.select_dictation_mode)
        ###################### 选择学习模式 #########################

        self.tab_changed(0)

    def tab_changed(self, index):
        # Handle the tab change here
        if index == 0:  # Assuming you want to switch to the first tab
            self.ui.stackedWidget.setCurrentIndex(0)
        elif index == 1:  # Assuming you want to switch to the second tab
            self.ui.stackedWidget.setCurrentIndex(1)
        elif index == 2:  # Assuming you want to switch to the third tab
            self.ui.stackedWidget.setCurrentIndex(2)

    def select_dictation_mode(self):
        self.word_study_setting.save_settings()
        self.word_study_setting.close()
        if self.word_study_setting.setting.selected_mode == "Cycling Remember":
            self.tab_changed(1)
            self.cycling_remember.set_play_setting(self.word_study_setting.setting)
            self.cycling_remember.set_words_data(self.dictations_words[self.tree_view_select_parent_index]["audio"])
            self.cycling_remember.play()
        elif self.word_study_setting.setting.selected_mode == "Dictation":
            self.tab_changed(2)

    def click_start_learn_word(self):
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

    def on_treeview_item_clicked(self, index):
        self.tab_changed(0)
        item = index.internalPointer()
        if item:
            if index.parent().isValid():
                self.tree_view_select_parent_index = index.row()
                self.tree_view_select_children_index = index.parent().row()
                print("Child Clicked. Index:", index.row(), "Parent Index:", index.parent().row())
            else:
                self.tree_view_select_parent_index = index.row()
                print("Parent Clicked. Index:", index.row())

        if self.tree_view_select_parent_index is not None:
            self.audio_words_all = [x.word for x in
                                    self.dictations_words[self.tree_view_select_parent_index]["audio"].words]
            self.model_all_words.setStringList(self.audio_words_all)
