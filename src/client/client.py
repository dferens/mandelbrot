


# def mandelbrot(z,maxiter):
#     c = z
#     for n in range(maxiter):
#         if abs(z) > 2:
#             return n
#         z = z*z + c
#     return maxiter

# def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter):
#     r1 = np.linspace(xmin, xmax, width)
#     r2 = np.linspace(ymin, ymax, height)
#     return (r1,r2,[mandelbrot(complex(r, i),maxiter) for r in r1 for i in r2])


# def mandelbrot_image(xmin, xmax, ymin, ymax, width=3, height=3, maxiter=80):
#     dpi = 72
#     img_width = dpi * width
#     img_height = dpi * height
#     x, y, z = mandelbrot_set(xmin,xmax,ymin,ymax,img_width,img_height,maxiter)

#     fig, ax = plt.subplots(figsize=(width, height),dpi=72)
#     ticks = np.arange(0,img_width,3*dpi)
#     x_ticks = xmin + (xmax-xmin)*ticks/img_width
#     plt.xticks(ticks, x_ticks)
#     y_ticks = ymin + (ymax-ymin)*ticks/img_width
#     plt.yticks(ticks, y_ticks)

#     norm = colors.PowerNorm(0.3)

#     ax.imshow(z.T,cmap='hot',origin='lower',norm=norm)

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

