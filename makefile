default:
	pip install -r requirements.txt
	pyinstaller --onefile --noconsole main.py