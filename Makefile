
PYTHON = python


DEPENDENCIES = requirements.txt


APP = app.py


install:
	@echo "Installing dependencies from $(DEPENDENCIES)..."
	$(PYTHON) -m pip install -r $(DEPENDENCIES)


run:
	@echo "Starting Flask development server..."
	FLASK_APP=$(APP) FLASK_ENV=development $(PYTHON) -m flask run

clean:
	@echo "Cleaning up Python bytecode and cache..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +



.PHONY: install run clean