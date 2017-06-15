REQUIREMENTS=requirements.txt
TRASH=**/*.pyc tests/__pycache__ failures

init:
	    pip install -r $(REQUIREMENTS)

check:
	    pytest

clean:
	rm -rf $(TRASH)

.PHONY: init test
