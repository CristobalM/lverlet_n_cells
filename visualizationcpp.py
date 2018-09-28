
import numpy as np
import matplotlib.pyplot as plt
import sys
import itertools
from cycler import cycler
from mpl_toolkits.mplot3d import Axes3D


def get_style_it():
    """
    Returns: iterator
    """
    return itertools.cycle(cycler(marker=[
        's', '8', 'X', 'P', 'D', 'p', '*', 'H',
        9, 1, 2, 3, 4, '_', 'x', '|', 10, 11, 4]) * cycler(color=[
        '#e6194b', '#3cb44b', '#ffe119', '#0082c8', '#f58231', '#911eb4', '#46f0f0',
        '#f032e6', '#d2f53c', '#fabebe', '#008080', '#e6beff', '#aa6e28', '#fffac8',
        '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000080', '#808080'
    ]))


if len(sys.argv) < 2:
    print("Data file required")
    exit()

dim = 2

if len(sys.argv) >= 3:
    dim = int(sys.argv[2])


def get_ticks(data, count=100):
    max_ = max(data)
    min_ = min(data)
    delta = (max_ - min_) / count
    ticks = np.arange(min_ - delta, max_ + delta*1.1, delta)
    return ticks

fname = sys.argv[1]#'foofile.txt'
if dim == 3:
    X = []
    Y = []
    Z = []
    with open(fname, 'r') as f:
        for line in f:
            line_arr = line.replace('\n', '').split(' ')
            [x, y, z] = line_arr
            X.append(np.float32(x))
            Y.append(np.float32(y))
            Z.append(np.float32(z))


    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)

    #XX, YY = np.meshgrid(X, Y)

    fig = plt.figure(figsize=(15,10))
    #ax = fig.gca(projection='3d')
    ax = fig.add_subplot(111, projection='3d')


    ax.scatter(X, Y, Z)
    plt.show()
elif dim == 2:
    X = []
    Y = []
    with open(fname, 'r') as f:
        for line in f:
            line_arr = line.replace('\n', '').replace('  ', ' ').replace('  ', ' ').split(' ')
            [x, y] = line_arr
            u = float(x)

            X.append(float(x))
            Y.append(float(y))

    X = np.array(X)
    Y = np.array(Y)

    #print(X)
    #print(Y)

    fig = plt.figure(figsize=(12, 12))
    #ax = fig.gca()

    plt.scatter(X, Y)
    max_x = max(X)
    min_x = min(X)
    count = 10
    xticks = get_ticks(X, count)
    yticks = get_ticks(Y, count)
    #plt.xticks(xticks)
    #plt.yticks(yticks)
    plt.grid(alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('y', rotation=0)
    plt.axvline(x=-100, c='r')
    plt.axvline(x=100, c='r')
    plt.axhline(y=-1000, c='r')
    plt.axhline(y=1000, c='r')
    plt.show()
