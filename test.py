# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QDoubleSpinBox
#

#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Settings Example")
#
#         self.settings_dialog = SettingsDialog()
#
#         main_widget = QPushButton("Open Settings")
#         main_widget.clicked.connect(self.open_settings_dialog)
#
#         self.setCentralWidget(main_widget)
#
#     def open_settings_dialog(self):
#         self.settings_dialog.exec()
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec())
import sys

# import speech_recognition as sr
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QLabel, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Speech Dictation Example")

        # self.r = sr.Recognizer()
        self.correct_word = "apple"  # Example correct word
        self.gap_time = 2  # Example gap time in seconds
        self.correct_count = 0
        self.total_count = 0
        self.start_time = 0

        main_widget = QWidget()
        layout = QVBoxLayout()main_widget

        self.line_edit = QLineEdit()
        self.line_edit.returnPressed.connect(self.check_word)
        layout.addWidget(self.line_edit)

        self.answer_label = QLabel()
        layout.addWidget(self.answer_label)

        self.correct_rate_label = QLabel()
        layout.addWidget(self.correct_rate_label)

        self.start_button = QPushButton("Start Dictation")
        self.start_button.clicked.connect(self.start_dictation)
        layout.addWidget(self.start_button)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Apply styles
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
            }
            QLabel {
                font-size: 18px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

    def check_word(self):
        user_input = self.line_edit.text().strip()
        if user_input == self.correct_word:
            self.correct_count += 1
            self.total_count += 1
            self.answer_label.setText("Correct! Next word:")
            self.line_edit.clear()
        else:
            self.total_count += 1
            self.answer_label.setText(f"Incorrect. Correct word: {self.correct_word}")
            self.line_edit.setStyleSheet("background-color: red")

    def start_dictation(self):
        self.answer_label.setText("Next word:")
        self.line_edit.setStyleSheet("")
        self.line_edit.clear()


    def update_correct_rate(self):
        correct_rate = (self.correct_count / self.total_count) * 100 if self.total_count > 0 else 0
        self.correct_rate_label.setText(f"Correct Rate: {correct_rate:.2f}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
