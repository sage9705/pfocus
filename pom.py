import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox
from PyQt5.QtCore import QTimer, Qt, QFile, QTextStream, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from PyQt5.QtGui import QIcon

class Timer(QWidget):
    timer_updated = pyqtSignal()
    session_completed = pyqtSignal(str)

    def __init__(self, work_time, break_time):
        super().__init__()
        self.work_time = work_time
        self.break_time = break_time
        self.current_time = work_time
        self.is_working = True
        self.completed_sessions = {"Work": 0, "Break": 0}

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("system-notification-4-206493.mp3")))

    def start(self):
        if self.current_time == 0:
            self.switch_mode()
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def reset(self):
        self.current_time = self.work_time
        self.is_working = True

    def switch_mode(self):
        self.is_working = not self.is_working
        if self.is_working:
            self.current_time = self.work_time
            self.completed_sessions["Work"] += 1
            self.session_completed.emit("Work")
        else:
            self.current_time = self.break_time
            self.completed_sessions["Break"] += 1
            self.session_completed.emit("Break")

    def update_timer(self):
        if self.current_time > 0:
            self.current_time -= 1
        else:
            self.switch_mode()
            self.player.play()
        self.timer_updated.emit()

class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(100, 100, 300, 150)

        self.timer = Timer(25 * 60, 5 * 60)
        self.timer.timer_updated.connect(self.update_time_display)
        self.timer.session_completed.connect(self.show_completion_notification)

        self.timer_label = QLabel()
        self.timer_label.setObjectName("timer_label")
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.start_timer)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setObjectName("pause_button")
        self.pause_button.clicked.connect(self.pause_resume_timer)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("reset_button")
        self.reset_button.clicked.connect(self.reset_timer)

        self.work_time_button = QPushButton("Set Work Time")
        self.work_time_button.setObjectName("work_time_button")
        self.work_time_button.clicked.connect(self.set_work_time)

        self.break_time_button = QPushButton("Set Break Time")
        self.break_time_button.setObjectName("break_time_button")
        self.break_time_button.clicked.connect(self.set_break_time)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.work_time_button)
        button_layout.addWidget(self.break_time_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.timer_label)
        main_layout.addLayout(button_layout)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        self.setLayout(main_layout)

        # Load CSS file
        self.load_stylesheet("style.css")

    def load_stylesheet(self, filename):
        style = QFile(filename)
        if not style.open(QFile.ReadOnly | QFile.Text):
            return
        stream = QTextStream(style)
        QApplication.instance().setStyleSheet(stream.readAll())

    def start_timer(self):
        self.timer.start()

    def pause_resume_timer(self):
        if self.timer.timer.isActive():
            self.timer.stop()
            self.pause_button.setText("Resume")
        else:
            self.timer.start()
            self.pause_button.setText("Pause")

    def reset_timer(self):
        self.timer.stop()
        self.timer.reset()
        self.update_time_display()

    def set_work_time(self):
        new_time, ok_pressed = QInputDialog.getInt(self, "Set Work Time", "Minutes:", self.timer.work_time // 60, 1, 60, 1)
        if ok_pressed:
            self.timer.work_time = new_time * 60
            if self.timer.is_working:
                self.timer.current_time = self.timer.work_time
                self.update_time_display()

    def set_break_time(self):
        new_time, ok_pressed = QInputDialog.getInt(self, "Set Break Time", "Minutes:", self.timer.break_time // 60, 1, 60, 1)
        if ok_pressed:
            self.timer.break_time = new_time * 60
            if not self.timer.is_working:
                self.timer.current_time = self.timer.break_time
                self.update_time_display()

    def update_time_display(self):
        minutes, seconds = divmod(self.timer.current_time, 60)
        time_str = '{:02d}:{:02d}'.format(minutes, seconds)
        self.timer_label.setText(time_str)

    def show_completion_notification(self, session_type):
        if session_type == "Work":
            message = "Work session completed. Take a break!"
        else:
            message = "Break time's over. Get back to work!"
        QMessageBox.information(self, "Session Complete", message)

def main():
    app = QApplication(sys.argv)
    window = PomodoroTimer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
