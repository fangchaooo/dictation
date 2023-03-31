import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QSlider, QLabel, QLineEdit, QSpinBox, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime


from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import threading
import time


from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView





Base = declarative_base()

class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    timestamp = Column(String, nullable=False)
    word = Column(String, nullable=False)
    user_input = Column(String, nullable=False)
    correct = Column(Boolean, nullable=False)


def setup_database():
    engine = create_engine('sqlite:///dictation_results.db')
    Base.metadata.create_all(engine)
    return engine

def fetch_results():
    engine = setup_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    results = session.query(Result).all()

    session.close()
    return results

def create_results_table_widget(results):
    table_widget = QTableWidget()

    table_widget.setRowCount(len(results))
    table_widget.setColumnCount(4)
    table_widget.setHorizontalHeaderLabels(['Timestamp', 'Correct Word', 'User Input', 'Correct'])

    for i, result in enumerate(results):
        table_widget.setItem(i, 0, QTableWidgetItem(result.timestamp))
        table_widget.setItem(i, 1, QTableWidgetItem(result.word))
        table_widget.setItem(i, 2, QTableWidgetItem(result.user_input))
        table_widget.setItem(i, 3, QTableWidgetItem('Yes' if result.correct else 'No'))

    table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    return table_widget


def create_correct_rate_chart(results):
    chart = QChart()
    series = QLineSeries()

    correct_count = 0
    for i, result in enumerate(results):
        if result.correct:
            correct_count += 1

        correct_rate = correct_count / (i + 1)
        series.append(i, correct_rate)

    chart.addSeries(series)
    chart.createDefaultAxes()
    chart.setTitle('Correct Rate')

    axisX = QValueAxis()
    axisX.setTickCount(len(results) + 1)
    chart.setAxisX(axisX, series)

    axisY = QValueAxis()
    axisY.setTickCount(11)
    axisY.setRange(0, 1)
    chart.setAxisY(axisY, series)

    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)

    return chart_view


class AudioDictationApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI elements and set their properties
        self.audio_file = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_slider)
        self.wait_time = 5000  # Default wait time (in milliseconds)

        self.init_ui()
        
        
        self.results = fetch_results()
        self.results_table_widget = create_results_table_widget(self.results)
        self.correct_rate_chart = create_correct_rate_chart(self.results)

        # Add the results table and chart to the main layout
        self.main_layout.addWidget(self.results_table_widget)
        self.main_layout.addWidget(self.correct_rate_chart)
        
    def init_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout()

        # Audio controls layout
        audio_controls_layout = QHBoxLayout()

        # Load button
        self.load_button = QPushButton('Load Audio File', self)
        self.load_button.clicked.connect(self.load_audio_file)
        audio_controls_layout.addWidget(self.load_button)

        # Play button
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.play_audio)
        audio_controls_layout.addWidget(self.play_button)

        # Pause button
        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.pause_audio)
        audio_controls_layout.addWidget(self.pause_button)

        main_layout.addLayout(audio_controls_layout)

        # Time range bar
        # self.time_range_bar = QSlider(Qt.Horizontal, self)
        self.time_range_bar = QSlider(Qt.Horizontal)
        self.time_range_bar.setTickPosition(QSlider.TicksBelow)
        self.time_range_bar.setTickInterval(1000)
        main_layout.addWidget(self.time_range_bar)

        # Start Dictation button
        self.start_dictation_btn = QPushButton('Start Dictation', self)
        self.start_dictation_btn.clicked.connect(self.start_dictation)
        main_layout.addWidget(self.start_dictation_btn)

        # User input box
        self.user_input = QLineEdit(self)
        main_layout.addWidget(self.user_input)

        # Correct word label
        self.correct_word_label = QLabel('', self)
        main_layout.addWidget(self.correct_word_label)

        # Wait time controls layout
        wait_time_controls_layout = QHBoxLayout()

        # Wait time label
        self.wait_time_label = QLabel('Wait Time (s):', self)
        wait_time_controls_layout.addWidget(self.wait_time_label)

        # Wait time spin box
        self.wait_time_spinbox = QSpinBox(self)
        self.wait_time_spinbox.setMinimum(1)
        self.wait_time_spinbox.setMaximum(60)
        self.wait_time_spinbox.setValue(5)  # Default value of 5 seconds
        self.wait_time_spinbox.valueChanged.connect(self.set_wait_time)
        wait_time_controls_layout.addWidget(self.wait_time_spinbox)

        main_layout.addLayout(wait_time_controls_layout)

        # Set the main layout
        self.setLayout(main_layout)

        # Set window properties
        self.setWindowTitle('Audio Dictation App')



    def load_audio_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open audio file", "", "Audio Files (*.mp3 *.wav);;All Files (*)", options=options)
        if file_name:
            self.audio_file = AudioSegment.from_file(file_name)
            self.time_range_bar.setMaximum(len(self.audio_file))
            self.end_time_label.setText(str(len(self.audio_file)))

    def play_audio(self):
        if hasattr(self, 'audio_file'):
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_slider)
            self.timer.start(1000)

            start_position = self.time_range_bar.value()
            end_position = len(self.audio_file)
            play_thread = threading.Thread(target=play, args=(self.audio_file[start_position:end_position],))
            play_thread.start()

    def pause_audio(self):
        if hasattr(self, 'timer'):
            self.timer.stop()

    def update_slider(self):
        current_position = self.time_range_bar.value()
        current_position += 1000
        if current_position < len(self.audio_file):
            self.time_range_bar.setValue(current_position)
            self.timestamp_label.setText(f"{current_position // 1000}s")
        else:
            self.timer.stop()
            
    def set_wait_time(self, new_wait_time):
        self.wait_time = new_wait_time * 1000  # Convert to milliseconds

            
    def start_dictation(self):
        self.pause_audio()  # Pause any ongoing playback

        engine = setup_database()
        Session = sessionmaker(bind=engine)
        session = Session()
        
        def play_and_wait(word_info):
            start_time = word_info["start_time"]
            end_time = word_info["end_time"]
            word_audio = self.audio_file[start_time:end_time]
            play(word_audio)

        for word_info in self.words:
            play_thread = threading.Thread(target=play_and_wait, args=(word_info,))
            play_thread.start()

            entered_word = ""
            wait_start_time = time.time()
            while play_thread.is_alive() or (time.time() - wait_start_time) * 1000 < self.wait_time:
                QApplication.processEvents()  # Keep the UI responsive
                entered_word = self.user_input.text().strip()
                if entered_word:
                    break
                time.sleep(0.1)

            play_thread.join()

            if entered_word.lower() == word_info["word"].lower():
                self.user_input.setStyleSheet("background-color: green")
                self.correct_word_label.setText(f"Correct! The word was: {word_info['word']}")
                result = Result(timestamp=str(datetime.now()), word=word_info["word"], user_input=entered_word, correct=True)
            else:
                self.user_input.setStyleSheet("background-color: red")
                self.correct_word_label.setText(f"Incorrect. The word was: {word_info['word']}")
                result = Result(timestamp=str(datetime.now()), word=word_info["word"], user_input=entered_word, correct=False)

            session.add(result)
            session.commit()

            self.user_input.clear()
            
        self.correct_word_label.setText("Dictation finished.")
        self.user_input.setStyleSheet("")  # Reset the input box's background color
        
        session.close()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioDictationApp()
    window.show()
    sys.exit(app.exec())
