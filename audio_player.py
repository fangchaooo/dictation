from pprint import pprint

from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QTimer, QTime, pyqtSignal, QThreadPool, Qt, QEvent
from PyQt6.QtGui import QIcon, QKeyEvent
import sys
import dictation, re
from pydub import AudioSegment, silence

from common import edit_line_register_keyboard_event
from work import Worker


def split_audio(*args, **kwargs):
    import json
    with open("tmp2.json", "r+") as f:
        data = json.load(f)
        return data["time"]
    # start_index = 0
    # all_data = data["time"]
    # for index in range(len(all_data)):
    #     if all_data[index][0] == "young fish":
    #         start_index = index + 1
    #
    # last = all_data[start_index - 1][0]
    # for i in range(start_index, len(all_data)):
    #     # if i+
    #     curent = all_data[i][0]
    #     all_data[i][0] = last
    #     last = curent
    #
    # with open("tmp2.json", "w") as f:
    #     json.dump({"time": all_data}, f)
    # return all_data

    # # Load your audio.
    # song = AudioSegment.from_file(args[0])
    # print(song.duration_seconds)
    # # Split track where the silence is 2 seconds or more and get chunks using
    # # the imported function.
    # range = silence.detect_nonsilent(song, min_silence_len=1000, silence_thresh=-100, seek_step=1)
    # # Process each chunk with your parameters
    # with open("tmp.json", "w") as f:
    #     json.dump( {"time":range}, f)
    # return range


class AudioPlayerApp(QMainWindow):
    signalSent = pyqtSignal(list)
    signalAudioWordSave = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.installEventFilter(self)
        self.muted = False
        self.audio_output.setVolume(50)
        self.ui: dictation.Ui_Form = None
        self.paly_source = None
        self.threadpool = QThreadPool()

        # play intervals
        self.timer = QTimer(self)
        self.play_intervals = []
        self.interval_index = 0
        self.repeat_counter = 0
        self.repeat_counter_current = 0
        self.gap_sec_time = 0
        self.timer.timeout.connect(self.play_next_interval)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            # It Playback Rate !
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Q:
                self.player.player.setPlaybackRate(0.8)
            elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_E:
                self.player.player.setPlaybackRate(1.2)
                # setPosition(int), argument is in milliseconds.
            elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_A:
                self.player.player.setPosition(self.player.player.position() - 10000)
            elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_D:
                self.player.player.setPosition(self.player.player.position() + 10000)

        return super().eventFilter(source, event)

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

        ################ split word #############################
        # edit time change
        ui.WordTimeStartInput.textChanged.connect(self.word_time_start_input_changed)
        # split word time
        ui.WordSaveBtn.clicked.connect(self.save_word_and_audio_time_range)
        edit_line_register_keyboard_event(self, ui.AudioWordInput, self.save_word_and_audio_time_range)
        # split word time
        ui.WordAudioStartBtn.clicked.connect(self.log_word_start_time)
        ################ split word #############################

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
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.ui.StartAudioBtn.setIcon(QIcon("./play.png"))
        else:
            self.player.play()
            self.ui.StartAudioBtn.setIcon(QIcon("./pause.png"))
            self.show_player_end_time()

    def log_word_start_time(self):
        # when playing audio, click btn to log word start time
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.ui.WordTimeStartInput.setText(self.convert_position_to_qtime(self.player.position()))
        # when start to play audio, click btn to log word end time
        elif self.player.playbackState() == QMediaPlayer.PlaybackState.PausedState:
            self.ui.WordTimeEndInput.setText(self.convert_position_to_qtime(self.player.position()))
        else:
            self.play_audio()

    def show_player_end_time(self):
        print(self.player.duration())
        self.ui.AudioEndTimeLabel.setText(self.convert_position_to_qtime(self.player.duration()))

    def pause_audio(self):
        self.player.pause()

    def reset_audio(self):
        self.player.stop()
        self.ui.StartAudioBtn.setIcon(QIcon("./play.png"))

    def open_music(self):
        # self.paly_source, _ = QFileDialog.getOpenFileName(self, "Open Audio File")
        self.paly_source = "/Users/btby/Documents/code/dictation/audios/a24.mp3"
        if self.paly_source != '':
            self.player.setSource(QUrl.fromLocalFile(self.paly_source))
            self.ui.StartAudioBtn.setEnabled(True)

        worker = Worker(split_audio, None, self.paly_source)
        worker.signals.result.connect(self.split_audio_to_words)
        # worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(worker)

    def split_audio_to_words(self, range):
        self.signalSent.emit(range)

    def set_source(self, path: str):
        self.player.setSource(QUrl.fromLocalFile(path))
        self.ui.StartAudioBtn.setEnabled(True)

    def play_interval(self, words_list, gap_sec_time=0, speed=1, repeat_times=1):
        self.play_intervals = words_list
        self.interval_index = 0
        self.repeat_counter = repeat_times
        self.gap_sec_time = gap_sec_time
        self.player.setPlaybackRate(speed)
        self.play_next_interval()

    def play_next_interval(self):
        if self.interval_index < len(self.play_intervals):
            start_time, end_time = self.play_intervals[self.interval_index]
            print(f"play_next_interval {start_time} {end_time}")
            if self.repeat_counter_current < self.repeat_counter:
                self.player.setPosition(start_time)  # Convert to milliseconds
                self.player.play()
                self.timer.start(end_time - start_time)  # Set timer duration
                self.repeat_counter_current += 1
            else:
                self.repeat_counter_current = 0
                self.interval_index += 1
                self.timer.start(self.gap_sec_time * 1000)  # Gap time of 1 second between intervals
        else:
            self.player.pause()
            self.timer.stop()

    def position_start(self, start_position, end_position):
        duration = start_position - end_position
        self.player.setPosition(self.convert_qtime_to_position(start_position))
        stop_timer = QTimer(self)
        stop_timer.timeout.connect(self.pause_audio)
        stop_timer.start(duration)

    def audio_play_slider_changed(self, position):
        self.player.setPosition(position)

    def position_changed(self, position):
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
        start_position = int(matches[0])
        end_position = int(matches[1])
        self.ui.WordTimeStartInput.setText(self.convert_position_to_qtime(start_position))
        self.ui.WordTimeEndInput.setText(self.convert_position_to_qtime(end_position))
        self.play_interval([[start_position, end_position]])

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


if __name__ == "__main__":
    res = split_audio("/home/trunk/Videos/222.m4a")
    print(len(res))
    pprint(res)
