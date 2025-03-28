default: compile

compile:
	pip install pyinstaller
	pyinstaller --onefile --noconsole main.py
