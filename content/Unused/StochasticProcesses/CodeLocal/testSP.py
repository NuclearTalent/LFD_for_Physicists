import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.abspath('../../Utils/'))

from StochasticProcess.StochasticProcess import StochasticProcess as SP

class testSP(SP):
    def start(self,random_state):
        return random_state.uniform()

    # First SP
    def update_SP(self, random_state, history):
        return np.sum(history) + random_state.uniform()

    # Markov chain
    def update_MC(self, random_state, history):
        return 0.5 * ( history[-1] + random_state.uniform() )

    # Markov chain from Metropolis algorithm
    def update(self, random_state, history):
        propose = history[-1] + 0.5*(random_state.uniform()-0.5)
        if propose<0 or propose>1:
            return history[-1]
        else:
            return propose

test=testSP(seed=1)
test.create_multiple_processes(50,5)
test.plot_processes()

import prettyplease.prettyplease as pp

test.create_multiple_processes(13,40000)
pp.corner(test.sequence.T,labels=[fr'$X_{{{i}}}$' for i in range(13)])

fig,axs, H_Xm_given_Xn,xedges,yedges = test.plot_conditional_distributions([1,4,8,12],bins=20)

plt.show()
        
