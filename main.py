from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QEvent, Qt
import sys
import dictation
import audio_player
import audio_words
import word_dictition


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = dictation.Ui_Form()
        self.ui.setupUi(self)
        self.player = audio_player.AudioPlayerApp()
        self.audio_words = audio_words.AudioWordList()
        self.dictation = word_dictition.WordDictation(self.player)
        self.player.setup_ui(self.ui)
        self.audio_words.setup_ui(self.ui)
        self.dictation.setup_ui(self.ui)

        self.init()

    def init(self):
        self.player.signalSent.connect(self.audio_words.updateListView)
        self.player.signalAudioWordSave.connect(self.audio_words.editTextChanged)
        self.player.signalSaveWordToDB.connect(self.audio_words.save_new_audio_to_db)
        self.audio_words.signalListViewItem.connect(self.player.update_word_time_range)


    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.Type.KeyPress:
    #         key = event.key()
    #         # It Playback Rate !
    #         if event.modifiers() == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Q:
    #             self.player.player.setPlaybackRate(0.8)
    #         elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_E:
    #             self.player.player.setPlaybackRate(1.2)
    #             # setPosition(int), argument is in milliseconds.
    #         elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_A:
    #             self.player.player.setPosition(self.player.player.position() - 10000)
    #         elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_D:
    #             self.player.player.setPosition(self.player.player.position() + 10000)
    #
    #     return super().eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.installEventFilter(window)
    window.show()
    sys.exit(app.exec())
