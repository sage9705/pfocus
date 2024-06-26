import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox, QAction, QMainWindow
from PyQt5.QtCore import QTimer, Qt, QFile, QTextStream, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

# Constants for time units
WORK_MINUTES = 25
BREAK_MINUTES = 5

class Timer(QWidget):
    timer_updated = pyqtSignal()
    session_completed = pyqtSignal(str)

    def __init__(self, work_time, break_time, work_sound, break_sound):
        super().__init__()
        self.work_time = work_time
        self.break_time = break_time
        self.current_time = work_time
        self.is_working = True
        self.completed_sessions = {"Work": 0, "Break": 0}

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.work_sound = QMediaPlayer()
        self.work_sound.setMedia(QMediaContent(QUrl.fromLocalFile(work_sound)))

        self.break_sound = QMediaPlayer()
        self.break_sound.setMedia(QMediaContent(QUrl.fromLocalFile(break_sound)))

        # Handle file loading errors
        if not self.work_sound.isAvailable() or not self.break_sound.isAvailable():
            QMessageBox.critical(self, "Error", "Failed to load sound files.")
            return

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
            if self.completed_sessions["Break"] > 0:
                self.completed_sessions["Break"] -= 1
            self.session_completed.emit("Work")
        else:
            self.current_time = self.break_time
            self.completed_sessions["Break"] += 1
            if self.completed_sessions["Work"] > 0:
                self.completed_sessions["Work"] -= 1
            self.session_completed.emit("Break")

    def update_timer(self):
        if self.current_time > 0:
            self.current_time -= 1
        else:
            self.switch_mode()
            if self.is_working:
                self.work_sound.play()
            else:
                self.break_sound.play()
        self.timer_updated.emit()

class PomodoroTimer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(300, 300, 500, 350)

        self.timer = Timer(WORK_MINUTES * 60, BREAK_MINUTES * 60, "work_sound.mp3", "break_sound.mp3")
        self.timer.timer_updated.connect(self.update_time_display)
        self.timer.session_completed.connect(self.show_completion_notification)

        self.timer_label = QLabel()
        self.timer_label.setObjectName("timer_label")
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setToolTip("Start the timer")
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.setObjectName("pause_button")
        self.pause_button.clicked.connect(self.pause_resume_timer)
        self.pause_button.setToolTip("Pause or resume the timer")

        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("reset_button")
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setToolTip("Reset the timer")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.create_menu_bar()
        self.load_stylesheet("style.css")

        # Set keyboard shortcuts
        self.start_button.setShortcut(Qt.Key_S)
        self.pause_button.setShortcut(Qt.Key_P)
        self.reset_button.setShortcut(Qt.Key_R)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("☰")
        settings_menu.setObjectName("settings_menu")

        set_work_time_action = QAction("Set Work Time", self)
        set_work_time_action.triggered.connect(self.set_work_time)
        settings_menu.addAction(set_work_time_action)

        set_break_time_action = QAction("Set Break Time", self)
        set_break_time_action.triggered.connect(self.set_break_time)
        settings_menu.addAction(set_break_time_action)

    def load_stylesheet(self, filename):
        css_file = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(css_file):
            style = QFile(css_file)
            if style.open(QFile.ReadOnly | QFile.Text):
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
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to reset the timer?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.timer.stop()
            self.timer.reset()
            self.update_time_display()

    def set_work_time(self):
        new_time, ok_pressed = QInputDialog.getInt(self, "Set Work Time", "Minutes:", WORK_MINUTES, 1, 60, 1)
        if ok_pressed:
            self.timer.work_time = new_time * 60
            if self.timer.is_working:
                self.timer.current_time = self.timer.work_time
                self.update_time_display()

    def set_break_time(self):
        new_time, ok_pressed = QInputDialog.getInt(self, "Set Break Time", "Minutes:", BREAK_MINUTES, 1, 60, 1)
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
            message = "Break time's over. Get back to work!"
            self.timer.break_sound.stop()
            self.timer.work_sound.play()
        else:
            message = "Work session completed. Take a break! "
            self.timer.work_sound.stop()
            self.timer.break_sound.play()

        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle("Session Complete")
        message_box.setText(message)
        message_box.exec_()

def main():
    QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    app = QApplication(sys.argv)
    window = PomodoroTimer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

