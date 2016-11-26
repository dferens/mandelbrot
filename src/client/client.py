import argparse
import csv

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


def render_mandelbort(points, width, height, file_name):
    dpi = 72.0
    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    points_matrix = np.array(points).reshape((width, height)).transpose()
    ax.imshow(points_matrix, cmap='gnuplot2', origin='lower', norm=colors.PowerNorm(0.3))
    fig.savefig(file_name)



def read_and_render_mandelbort(result_file_path, width, height, picture_path):
    """
    @param str result_file_path:
    @param int width:
    @param int height:
    """
    with open(result_file_path, 'rb') as csvfile:
        lines = list(csv.reader(csvfile))

    assert lines[0] == ['real', 'imag', 'iter'], 'Wrong file format'
    points = [int(l[2]) for l in lines[1:]]
    render_mandelbort(points, width, height, picture_path)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('file', metavar='file', type=str, help='path to result csv file')
    parser.add_argument('width', metavar='width', type=int, help='image width in pixels')
    parser.add_argument('height', metavar='height', type=int, help='image height in pixels')
    parser.add_argument('picture', metavar='picture', type=str, help='path to result picture')

    args = parser.parse_args()
    read_and_render_mandelbort(args.file, args.width, args.height, args.picture)

if __name__ == '__main__':
    main()
