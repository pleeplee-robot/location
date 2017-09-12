REQUIREMENTS=requirements.txt
TRASH=**/*.pyc tests/__pycache__ failures

check:
	pytest

init:
	pip3 install -r $(REQUIREMENTS)

clean:
	rm -rf $(TRASH)

.PHONY: init test
