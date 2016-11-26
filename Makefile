NVCC = /usr/local/cuda/bin/nvcc
CUBIN_FILE = main.cubin
PYTHON = PYTHONHOME=$(VIRTUAL_ENV) /usr/local/bin/python

all: cpu

clean:
	find ./var -type f -delete
	find ./src -name "*.pyc" -delete

cpu:
	gcc src/core/cpu/main.c -o var/cpu
	./var/cpu 1000 1000 100 var/cpu-result.csv
	$(PYTHON) src/client/client.py var/cpu-result.csv 1000 1000 var/cpu-result.png

gpu:
	$(NVCC) -o var/gpu src/core/gpu/main.cu
	./var/gpu 1000 1000 100 var/gpu-result.csv
	$(PYTHON) src/client/client.py var/gpu-result.csv 1000 1000 var/gpu-result.png
