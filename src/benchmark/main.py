import re
from subprocess import Popen, PIPE

from matplotlib import pyplot as plt


def unzip(list_of_tuples):
    """
    Splits list of tuples into separate lists
    """
    return zip(*list_of_tuples)

def run_mandelbort(target, width, height, max_iter, csv_file=None):
    """
    @param str target: 'cpu' or 'gpu'
    @param int width:
    @param int height:
    @param int max_iter:
    @param str | None csv_file:
    @returns: computation time in seconds
    @rtype: float
    """
    assert target in {'cpu', 'gpu'}

    command = {
        'cpu': './var/cpu',
        'gpu': './var/gpu'
    }[target]
    args = [command, width, height, max_iter]

    if csv_file is not None:
        args.append(csv_file)

    process = Popen(map(str, args), stdout=PIPE, shell=False)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code != 0:
        raise RuntimeError(output)
    else:
        seconds = float(re.search(r'Spent: ([\d.]+) seconds', output).group(1))
        return seconds


def run_mandelbort_targets(width, height, max_iter):
    """
    @returns: (cpu time, gpu time)
    @rtype: (float, float)
    """
    return (
        run_mandelbort('cpu', width, height, max_iter),
        run_mandelbort('gpu', width, height, max_iter)
    )


def benchmark_by_max_iter(points):
    MIN_ITER, MAX_ITER = 0, 2000
    width, height = 1000, 1000

    x = range(MIN_ITER, MAX_ITER + 1, (MAX_ITER - MIN_ITER) / points)
    y_cpu, y_gpu = unzip([
        run_mandelbort_targets(width, height, max_iter)
        for max_iter in x
    ])
    plt.clf()
    plt.plot(x, y_cpu, label='CPU')
    plt.plot(x, y_gpu, label='GPU')
    plt.legend(loc='upper left')
    plt.title('Render {}x{} image'.format(width, height))
    plt.xlabel('Max. iter')
    plt.ylabel('Seconds spent')
    plt.savefig('var/benchmark-by-maxiter.png')


def benchmark_by_image_size(points):
    MIN_SIZE, MAX_SIZE = 10, 1000
    max_iter = 1000

    x = range(MIN_SIZE, MAX_SIZE + 1, (MAX_SIZE - MIN_SIZE) / points)
    y_cpu, y_gpu = unzip([
        run_mandelbort_targets(a, a, max_iter)
        for a in x
    ])
    plt.clf()
    plt.plot(x, y_cpu, label='CPU')
    plt.plot(x, y_gpu, label='GPU')
    plt.legend(loc='upper left')
    plt.title('Render image with {} max iter.'.format(max_iter))
    plt.xlabel('Image size px.')
    plt.ylabel('Seconds spent')
    plt.savefig('var/benchmark-by-imagesize.png')

def main():
    benchmark_by_max_iter(10)
    benchmark_by_image_size(10)

if __name__ == '__main__':
    main()
