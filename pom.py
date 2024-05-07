import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt, pyqtSignal

class Timer(QWidget):
    timer_updated = pyqtSignal()

    def __init__(self, work_time, break_time):
        super().__init__()
        self.work_time = work_time
        self.break_time = break_time
        self.current_time = work_time
        self.is_working = True

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

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
        else:
            self.current_time = self.break_time

    def update_timer(self):
        if self.current_time > 0:
            self.current_time -= 1
        else:
            self.switch_mode()
        self.timer_updated.emit()

class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(100, 100, 300, 150)

        self.timer = Timer(25 * 60, 5 * 60)
        self.timer.timer_updated.connect(self.update_time_display)

        self.timer_label = QLabel()
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 36px; color: #333")

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px")
        self.start_button.clicked.connect(self.start_timer)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #f44336; color: white; border: none; border-radius: 5px")
        self.reset_button.clicked.connect(self.reset_timer)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.reset_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.timer_label)
        main_layout.addLayout(button_layout)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        self.setLayout(main_layout)

    def start_timer(self):
        self.timer.start()

    def reset_timer(self):
        self.timer.stop()
        self.timer.reset()
        self.update_time_display()

    def update_time_display(self):
        minutes, seconds = divmod(self.timer.current_time, 60)
        time_str = '{:02d}:{:02d}'.format(minutes, seconds)
        self.timer_label.setText(time_str)

def main():
    app = QApplication(sys.argv)
    window = PomodoroTimer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
