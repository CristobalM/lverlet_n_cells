import matplotlib.pyplot as plt
import numpy as np


def multiple_lambdas_plot(lambdas, times, sim_steps, particles_num, max_lambda=2.0):
    plt.plot(lambdas, times)
    plt.xlabel("Lambda")
    plt.ylabel("Tiempo")
    plt.xticks(np.arange(0.0, max_lambda + 0.05, max_lambda / 12.0))
    plt.title("Numero de iteraciones: %d, Numero de particulas: %d" % (sim_steps, particles_num))
    #plt.show()