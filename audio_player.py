from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QTimer, QTime, pyqtSignal
from PyQt6.QtGui import QIcon
import sys
import dictation, re
from pydub import AudioSegment, silence

from common import  edit_line_register_keyboard_event
def split_audio(file_path):
    # Load your audio.
    res = []
    song = AudioSegment.from_file(file_path)
    # Split track where the silence is 2 seconds or more and get chunks using
    # the imported function.
    range = silence.detect_silence(song, min_silence_len=100, silence_thresh=-16, seek_step=1)
    # Process each chunk with your parameters
    return range


class AudioPlayerApp(QMainWindow):
    signalSent = pyqtSignal(list)
    signalAudioWordSave = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.muted = False
        self.ui: dictation.Ui_Form = None
        self.paly_source = None

    def setup_ui(self, ui: dictation.Ui_Form):
        self.ui = ui
        ui.LoadAudioBtn.clicked.connect(self.open_music)
        ui.StartAudioBtn.clicked.connect(self.play_audio)
        ui.StartAudioBtn.setEnabled(False)
        ui.ResetAudioBtn.clicked.connect(self.reset_audio)

        ui.AudiohorizontalSlider.sliderMoved.connect(self.audio_play_slider_changed)

        ui.AudioVolumSlider.sliderMoved.connect(self.audio_volume_changed)
        ui.AudioVolumSlider.setValue(50)
        ui.AudioVolumBtn.clicked.connect(self.audio_mute_or_open)
        # edit time change
        ui.WordTimeStartInput.textChanged.connect(self.word_time_start_input_changed)

        ui.WordSaveBtn.clicked.connect(self.save_word_and_audio_time_range)

        edit_line_register_keyboard_event(self, ui.AudioWordInput, self.save_word_and_audio_time_range)

        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

    def audio_mute_or_open(self):
        self.muted = not self.muted
        if not self.muted:
            self.ui.AudioVolumBtn.setIcon(QIcon("./mute.png"))
            self.ui.AudioVolumSlider.setValue(0)
        else:
            self.ui.AudioVolumBtn.setIcon(QIcon("./volume.png"))
            self.ui.AudioVolumSlider.setValue(50)
        self.audio_output.setMuted(self.muted)

    def audio_volume_changed(self, num: float):
        self.audio_output.setVolume(num)

    def word_time_start_input_changed(self, value):
        self.player.setPosition(self.convert_qtime_to_position(value))

    def play_audio(self):
        print(self.player.PlaybackState)
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.ui.StartAudioBtn.setIcon(QIcon("./play.png"))
        else:
            # self.audio_output.setVolume(50)
            self.player.play()
            self.ui.StartAudioBtn.setIcon(QIcon("./pause.png"))
            self.show_player_end_time()

    def show_player_end_time(self):
        self.ui.AudioEndTimeLabel.setText(self.convert_position_to_qtime(self.player.duration()))

    def pause_audio(self):
        self.player.pause()

    def reset_audio(self):
        self.player.stop()
        self.ui.StartAudioBtn.setIcon(QIcon("./play.png"))

    def open_music(self):
        self.paly_source, _ = QFileDialog.getOpenFileName(self, "Open Audio File")
        if self.paly_source != '':
            self.player.setSource(QUrl.fromLocalFile(self.paly_source))
            self.ui.StartAudioBtn.setEnabled(True)
        range = split_audio(self.paly_source)
        self.signalSent.emit(range)

    def set_source(self, path: str):
        self.player.setSource(QUrl.fromLocalFile(path))
        self.ui.StartAudioBtn.setEnabled(True)

    def play_word(self, words_list, gap_time, speed, repeat_times):
        pass

    def position_start(self, start_position, end_position):
        duration = start_position - end_position
        self.player.setPosition(self.convert_qtime_to_position(start_position))
        stop_timer = QTimer(self)
        stop_timer.timeout.connect(self.pause_audio)
        stop_timer.start(duration)

    def audio_play_slider_changed(self, position):
        self.player.setPosition(position)

    def position_changed(self, position):
        print(position)
        if self.ui.AudiohorizontalSlider.maximum() != self.player.duration():
            self.ui.AudiohorizontalSlider.setMaximum(self.player.duration())

        self.ui.AudiohorizontalSlider.setValue(position)

        self.ui.AudioStartTimeLabel.setText(self.convert_position_to_qtime(position))
        self.ui.WordTimeEndInput.setText(self.convert_position_to_qtime(position))

    def duration_changed(self, duration):
        # self.ui.horizontalSliderPlay.setRange(0, duration)
        print(duration)

    def convert_position_to_qtime(self, position):
        mseconds = position % 1000
        seconds = (position // 1000) % 60
        minutes = (position // 60000) % 60
        hours = (position // 3600000) % 24

        time = QTime(hours, minutes, seconds, mseconds)
        time_str = time.toString("hh:mm:ss.zzz")
        return time_str

    def convert_qtime_to_position(self, time: str):
        time = QTime.fromString(time)
        position = time.hour() * 3600000 + time.minute() * 60000 + time.second() * 1000 + time.msec() // 1000
        return position

    def update_word_time_range(self, time_range: str):
        pattern = r'\b\d+\b'
        matches = re.findall(pattern, time_range)
        self.ui.WordTimeStartInput.setText(self.convert_position_to_qtime(int(matches[0])))
        self.ui.WordTimeEndInput.setText(self.convert_position_to_qtime(int(matches[1])))

    def save_word_and_audio_time_range(self):
        text = self.ui.AudioWordInput.text()
        start = self.ui.WordTimeStartInput.text()
        end = self.ui.WordTimeEndInput.text()
        self.signalAudioWordSave.emit([text, start, end])




    def find(self):
        input_string = "apple [1, 2]"
        word_pattern = r'\b\w+\b'
        number_pattern = r'\b\d+\b'

        words = re.findall(word_pattern, input_string)
        numbers = re.findall(number_pattern, input_string)
