REQUIREMENTS=requirements.txt
TRASH=**/*.pyc **/__pycache__ failures

check:
	pytest

init:
	pip3 install -r $(REQUIREMENTS)

doc:
	$(MAKE) -C doc/ html

clean:
	$(RM) -r $(TRASH)
	$(MAKE) -C doc/ clean

.PHONY: init test doc
