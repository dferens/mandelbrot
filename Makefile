PYTHON=PYTHONHOME=$(VIRTUAL_ENV) /usr/local/bin/python

clean:
	find ./var -type f -delete
	find ./src -name "*.pyc" -delete

cpu:
	gcc src/core/cpu.c -o var/cpu
	./var/cpu 1000 1000 100 var/cpu-result.csv
	$(PYTHON) src/client/client.py var/cpu-result.csv 1000 1000 var/cpu-result.png
