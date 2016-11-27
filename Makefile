PYTHON = PYTHONHOME=$(VIRTUAL_ENV) /usr/local/bin/python

all: clean compile benchmark

clean:
	@find ./var -type f -delete
	@find ./src -name "*.pyc" -delete

compile:
	@echo 'Compiling:'
	gcc src/core/cpu/main.c -o var/cpu
	$(NVCC) -o var/gpu src/core/gpu/main.cu

cpu:
	./var/cpu 1000 1000 1000 var/cpu-result.csv
	$(PYTHON) src/client/client.py var/cpu-result.csv 1000 1000 var/cpu-result.png

gpu:
	./var/gpu 1000 1000 1000 var/gpu-result.csv
	$(PYTHON) src/client/client.py var/gpu-result.csv 1000 1000 var/gpu-result.png

benchmark:
	@echo 'Running benchmarks:'
	$(PYTHON) src/benchmark/main.py
