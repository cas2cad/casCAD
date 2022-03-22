init: 
	pip install -r requirements.txt

test:
	python -m unittest tests/test_kb.py

.PHONY: init test