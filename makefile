default: compile

compile:
	pip install -r requirements.txt
	pip install pyinstaller
	pyinstaller --onefile --noconsole main.py
