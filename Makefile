REQUIREMENTS=requirements.txt

init:
	    pip install -r $(REQUIREMENTS)

check:
	    pytest

clean:
	rm -rf **/*.pyc tests/__pycache__

.PHONY: init test
