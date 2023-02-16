# word-count-tracker
Track how much words you've written every day. The program calculates the difference of your daily word totals and saves it to a database.

## Usage
Windows builds are [available here](https://github.com/aleksandrsw/word-count-tracker/releases/tag/v1.0.0).
The program can also be run in a Python interpreter:

```
$ pip install platformdirs
$ python word_count_tracker.py
```

In order to compile into an executable, do:
```
$ pip install pyinstaller
$ pyinstall --onefile word_count_tracker.py
```
