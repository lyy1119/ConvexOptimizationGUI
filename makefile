default:
	pip install -r requirements.txt
	pyinstaller --onefile --noconsole -n convexOptimization main.py