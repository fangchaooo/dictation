from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import sys
import dictation
import audio_player
import audio_words


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = dictation.Ui_Form()
        self.ui.setupUi(self)
        self.player = audio_player.AudioPlayerApp()
        self.audio_words = audio_words.AudioWordList()
        self.player.setup_ui(self.ui)
        self.audio_words.setup_ui(self.ui)

        self.init()

    def init(self):
        self.player.signalSent.connect(self.audio_words.updateListView)
        self.player.signalAudioWordSave.connect(self.audio_words.editTextChanged)

        self.audio_words.signalListViewItem.connect(self.player.update_word_time_range)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
