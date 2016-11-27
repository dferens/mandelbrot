import re
import argparse
from subprocess import Popen, PIPE

from matplotlib import pyplot as plt

try:
    # Requires terminal-notifier:
    #    https://github.com/julienXX/terminal-notifier
    from pync import Notifier
except ImportError:
    notify_finished = lambda: 0
else:
    notify_finished = lambda: Notifier.notify('Finished', title='Mandelbrot', sound='default')


class Target(tuple):

    @property
    def id(self):
        return self[0]

    @property
    def label(self):
        return self[1]

    @property
    def executable(self):
        return self[2]

    @classmethod
    def new(cls, id, label, executable):
        return Target([id, label, executable])


CPU = Target.new('cpu', 'CPU', './var/cpu')
GPU = Target.new('gpu', 'GPU', './var/gpu')


def run_mandelbort(target, width, height, max_iter, csv_file=None):
    """
    @param set[Target] targets:
    @param int width:
    @param int height:
    @param int max_iter:
    @param str | None csv_file:
    @returns: computation time in seconds
    @rtype: float
    """
    assert isinstance(target, Target)

    args = [target.executable, width, height, max_iter]

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


def benchmark_by_max_iter(points, targets):
    MIN_ITER, MAX_ITER = 0, 1000
    WIDTH, HEIGHT = 1000, 1000

    x_series = range(MIN_ITER, MAX_ITER + 1, (MAX_ITER - MIN_ITER) / points)
    plt.clf()
    fig, ax = plt.subplots()

    for t in targets:
        y_series = [run_mandelbort(t, WIDTH, HEIGHT, max_iter) for max_iter in x_series]
        plt.plot(x_series, y_series, label=t.label, marker='.')

        for (x, y) in zip(x_series, y_series):
            ax.annotate('{:.3}'.format(y), (x, y))

    plt.xticks(x_series)
    plt.legend(loc='upper left')
    plt.title('Render {}x{} image'.format(WIDTH, HEIGHT))
    plt.xlabel('Max. iter')
    plt.ylabel('Seconds spent')
    plt.savefig('var/benchmark-by-maxiter.png')


def benchmark_by_image_size(points, targets):
    MIN_SIZE, MAX_SIZE = 10, 1000
    MAX_ITER = 1000

    x_series = range(MIN_SIZE, MAX_SIZE + 1, (MAX_SIZE - MIN_SIZE) / points)
    plt.clf()
    fig, ax = plt.subplots()

    for t in targets:
        y_series = [run_mandelbort(t, x, x, MAX_ITER) for x in x_series]
        plt.plot(x_series, y_series, label=t.label, marker='.')

        for (x, y) in zip(x_series, y_series):
            ax.annotate('{:.3}'.format(y), (x, y))

    plt.xticks(x_series)
    plt.legend(loc='upper left')
    plt.title('Render image with {} max iter.'.format(MAX_ITER))
    plt.xlabel('Image size px.')
    plt.ylabel('Seconds spent')
    plt.savefig('var/benchmark-by-imagesize.png')

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('points', metavar='p', type=int, help='Number of points on chart')
    parser.add_argument('--cpu', action='store_true', help='Run only on CPU')
    parser.add_argument('--gpu', action='store_true', help='Run only on GPU')
    args = parser.parse_args()

    targets = {CPU, GPU}

    if args.cpu:
        targets = {CPU}
    elif args.gpu:
        targets = {GPU}

    benchmark_by_max_iter(args.points, targets)
    benchmark_by_image_size(args.points, targets)
    notify_finished()

if __name__ == '__main__':
    main()
