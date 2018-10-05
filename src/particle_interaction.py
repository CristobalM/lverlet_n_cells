from abc import abstractmethod
import numpy as np

class ParticleInteraction:
    @abstractmethod
    def eval(self, r):
        pass


class WCAParticleInteraction(ParticleInteraction):
    def __init__(self, epsilon, sigma):
        self.epsilon = epsilon
        self.sigma = sigma
        self.cond_val = (2.0**(1.0/6.0))*sigma

    def eval(self, r):
        if r >= self.cond_val:
            return 0
        if r == 0:
            return -100000
        sigma6 = self.sigma**6
        sigma12 = sigma6**2

        return -4*self.epsilon*(6*(sigma6/(r**7)) - 12*(sigma12/(r**13)))

    def get_rc(self):
        return self.cond_val
