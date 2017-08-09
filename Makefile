REQUIREMENTS=requirements.txt
TRASH=**/*.pyc tests/__pycache__ failures

check:
	    pytest

init:
	    pip install -r $(REQUIREMENTS)

clean:
	rm -rf $(TRASH)

.PHONY: init test
