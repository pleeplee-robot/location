REQUIREMENTS=requirements.txt
TRASH=**/*.pyc **/__pycache__ failures

check:
	pytest

init:
	pip3 install -r $(REQUIREMENTS)

clean:
	rm -rf $(TRASH)

.PHONY: init test
