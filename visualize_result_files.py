import matplotlib.pyplot as plt
import numpy as np
import re
import os
import sys
from matplotlib import rcParams

from cycler import cycler
import itertools

if len(sys.argv) < 2:
    print("Especifique la carpeta con resultados con la siguiente sintaxis:")
    print("python %s carpeta_resultados" % sys.argv[0])
    exit(1)

results_folder = sys.argv[1]

digit = r'\d*\.?\d+'

regex = r'^result_(%s)_(%s)_%s_\w+_%s_%s_%s_%s_\w+_%s_\.txt$' % (digit, digit, digit, digit, digit, digit, digit, digit)
"""
print(regex)
tomatch = 'result_1.1000_0.6000_50.0000_WallPeriodicBC_1_0.5000_1_0.0100_False_1024_.txt'

matches = re.match(regex, tomatch)
if matches:
    print(matches.group(1))
    print(matches.group(2))
else:
    print("no match")
"""

files = os.listdir(results_folder)

time_lambda_curves = {}

for filename in files:
    matches = re.match(regex, filename)
    if not matches:
        continue

    the_lambda = float(matches.group(1))
    the_eta = float(matches.group(2))
    with open(results_folder + filename, 'r') as f:
        first_line = f.readline()
        the_time = float(first_line)
    
    if the_eta not in time_lambda_curves:
        time_lambda_curves[the_eta] = {
            'times': [],
            'lambdas': []
        }
    
    time_lambda_curves[the_eta]['times'].append(the_time)    
    time_lambda_curves[the_eta]['lambdas'].append(the_lambda)

marker = itertools.cycle(('s', 'X', '+', 'o', '*', '>', 'h', 'd', '.'))
lines = itertools.cycle((':', '-.', '--', '-'))

# Configuraciones de estilo de los graficos
plt.figure(figsize=(12, 10), dpi=80, facecolor='w', edgecolor='k')
plt.rc('lines', linewidth=1)
plt.rc('axes', prop_cycle=(cycler('color', ['blue', 'green', 'red',
                                            'magenta', 'black',
                                            'purple', 'pink', 'brown',
                                            'orange', 'coral',
                                            'lightblue', 'lime', 'lavender',
                                            'turquoise', 'darkgreen', 'tan',
                                            'salmon', 'gold',
                                            'darkred', 'darkblue'])))

to_plot = []

for eta, values in time_lambda_curves.items():
    to_plot.append((eta, values))

to_plot.sort()

#for eta, values in time_lambda_curves.items():
for eta, values in to_plot:
    the_times = values['times']
    the_lambdas = values['lambdas']

    order = np.argsort(the_lambdas)

    xs = np.array(the_lambdas)[order]
    ys = np.array(the_times)[order]

    plt.plot(xs, ys, label="$\eta = %.1f$" % eta, marker=next(marker), markersize=15, linewidth=3)
    plt.xticks(np.arange(0.0, 1.4, 0.1))
    plt.yticks(np.arange(0, 10001, 1000))
    plt.xlabel('$\lambda$', fontsize=18)
    plt.ylabel('Tiempo (s)', fontsize=18)
    plt.title('Tiempo de ejecución del algoritmo de Listas de Verlet\n para un tiempo de simulación físico de 50 segundos', fontsize=22, y=1.02)

#plot.legend(loc=2, prop={'size': 6})
plt.legend(prop={'size': 16})
plt.grid(alpha=0.5)
plt.show()
