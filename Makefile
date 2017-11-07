REQUIREMENTS=requirements.txt
TRASH=**/*.pyc **/__pycache__ failures

check:
	pytest

init:
	pip3 install -r $(REQUIREMENTS)

doc:
	$(MAKE) -C docs/ html

clean:
	$(RM) -r $(TRASH)
	$(MAKE) -C docs/ clean

.PHONY: init test doc check
