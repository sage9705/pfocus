import tkinter as tk
from tkinter import messagebox
import time

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Timer")

        self.work_time = 25 * 60  # 25 minutes in seconds
        self.break_time = 5 * 60  # 5 minutes in seconds
        self.current_time = self.work_time
        self.is_working = True

        self.label = tk.Label(master, text="00:00", font=("Helvetica", 48))
        self.label.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.RIGHT, padx=10)

        self.update_time()

    def start_timer(self):
        if self.current_time == 0:
            self.switch_mode()
        self.timer()

    def reset_timer(self):
        self.current_time = self.work_time
        self.is_working = True
        self.update_time()

    def switch_mode(self):
        self.is_working = not self.is_working
        if self.is_working:
            self.current_time = self.work_time
        else:
            self.current_time = self.break_time

    def timer(self):
        if self.current_time > 0:
            minutes, seconds = divmod(self.current_time, 60)
            time_str = '{:02d}:{:02d}'.format(minutes, seconds)
            self.label.config(text=time_str)
            self.current_time -= 1
            self.master.after(1000, self.timer)
        else:
            self.switch_mode()
            self.timer()

    def update_time(self):
        minutes, seconds = divmod(self.current_time, 60)
        time_str = '{:02d}:{:02d}'.format(minutes, seconds)
        self.label.config(text=time_str)

def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
