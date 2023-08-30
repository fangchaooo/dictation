import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QObject, QEvent, pyqtSignal


class EnterSignalEmitter(QObject):
    enter_pressed = pyqtSignal()

    def eventFilter(self, obj, event):
        if obj is not None and event.type() == QEvent.Type.KeyPress:
            key_event = event
            if (key_event.key() == Qt.Key.Key_Return or
                    key_event.key() == Qt.Key.Key_Enter):
                self.enter_pressed.emit()
                return True
        return super().eventFilter(obj, event)


def edit_line_register_keyboard_event(ui_class, line_edit_ui, callback):
    line_edit_ui.installEventFilter(EnterSignalEmitter(ui_class))
    ui_class.line_edit_signal_emitter = EnterSignalEmitter(ui_class)
    ui_class.line_edit_signal_emitter.enter_pressed.connect(callback)
    line_edit_ui.installEventFilter(ui_class.line_edit_signal_emitter)
