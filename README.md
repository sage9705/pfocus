# pfocus
## Overview
The Pomodoro Timer application (pfocus) is a productivity tool designed to help users manage their time effectively using the Pomodoro Technique. It allows users to set work and break durations and notifies them when each session is completed.


## Features
- Set customizable work and break durations.
- Start, pause, and reset the timer.
- Display notifications when work or break sessions are completed.
- Keyboard shortcuts for convenient timer control.
- Error handling for sound file loading failures.
- Confirmation dialog for resetting the timer.

## Changes Made
1. **Constants for Time Units**: Used constants `WORK_MINUTES` and `BREAK_MINUTES` to set default work and break durations for improved readability and maintainability.
2. **UI Layout Refactoring**: Restructured the UI layout for better organization and alignment, enhancing user experience.
3. **Session Counters**: Added functionality to display the number of completed work and break sessions, providing users with progress tracking.
4. **Styling and Theming**: Implemented a separate CSS file handling using the `os.path` module for styling and theming.
5. **File Loading Error Handling**: Implemented error handling for sound file loading failures to notify users when there's an issue.
6. **Button Tooltips**: Added tooltips for buttons to provide users with hints about their functionality for better usability.
7. **Keyboard Shortcuts**: Implemented keyboard shortcuts for common actions like starting, pausing, and resetting the timer for enhanced accessibility.
8. **Sound Playback Optimization**: Optimized sound playback to ensure smooth performance during work and break sessions.
9. **Confirmation Dialog**: Added a confirmation dialog for resetting the timer to prevent accidental resets and data loss.

## How to Use
1. **Setting Work and Break Durations**: Click on "☰" in the menu bar and select "Set Work Time" or "Set Break Time" to adjust the durations.
2. **Starting the Timer**: Click on the "Start" button or use the keyboard shortcut "S" to start the timer.
3. **Pausing/Resuming the Timer**: Click on the "Pause" button or use the keyboard shortcut "P" to pause or resume the timer.
4. **Resetting the Timer**: Click on the "Reset" button or use the keyboard shortcut "R" to reset the timer. A confirmation dialog will appear to confirm the action.
5. **Session Notifications**: Notifications will appear when each work or break session is completed.


## Dependencies

- Python 3.x
- PyQt5

## Usage

```bash
python pom.py

```

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please feel free to open an issue or create a pull request.


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/sage9705/pfocus/blob/master/LICENSE) file for details.


