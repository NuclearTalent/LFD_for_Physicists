import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod

class StochasticProcess(ABC):
    """Parent (base) class for a generic stochastic process.

    The user can create a derived class (subclass) but must implement the 
    :meth:`start` and :meth:`update` methods.

    Methods:
    
    Abstract methods (must be defined in the subclass)
    ---------------------------------------------------
    start
    update

    Class methods (see full docstrings in the function def.)
    ---------------------------------------------------
    create_single_process
    create_multiple_processes
    plot_processes
    plot_conditional_distributions

    Attributes
    ----------
    state : RandomState
    position : int
        Current position in the sequence.
    sequence : ndarray 
        Values in the sequence. 
    """
    def __init__(self,seed=42):
        """Initialize a generic stochastic process
        
        Parameters
        ----------
        seed : int or None
            Random seed for reproducibility. Will be used to initialize a random state.
        """
        self.state = np.random.RandomState(seed=seed)

    def create_single_process(self,length_of_process):
        """Create a single instance of the process.

        Will initialize the process with :meth:`start`.
        Then calls :meth:`update` `length_of_process`-1 times to populate `self.sequence`

        Parameters
        ----------
        length_of_process : int
            Length of the instance of the process (including the initial value)
        """
        self.sequence = np.empty(length_of_process)
        self.position = 0
        self.sequence[0] = self.start(self.state)
        for _ in range(length_of_process-1):
            self.position += 1
            history = self.sequence[:self.position]
            self.sequence[self.position] = self.update(self.state,history)

    def create_multiple_processes(self,length_of_process,num_processes):
        """Create multiple instances of the process.

        Will initialize the process with :meth:`start`.
        Then iterates `num_processes` times, 
        for each: 
            calls :meth:`update` `length_of_process`-1 times 
            populates a column of `self.sequence`

        Parameters
        ----------
        length_of_process : int
            Length of the instance of the process (including the initial value)
        num_processes : int
            Number of processes to run
        """
        self.sequence = np.empty((length_of_process,num_processes))
        for n_process in range(num_processes):
            self.position = 0
            self.sequence[0,n_process] = self.start(self.state)
            for _ in range(length_of_process-1):
                self.position += 1
                history = self.sequence[:self.position,n_process]
                self.sequence[self.position,n_process] = self.update(self.state,history)

    def plot_processes(self):
        """Plot the sequences that have been generated.
        
        Returns fig,ax handles
        """
        fig,ax = plt.subplots(1,1)
        ax.plot(self.sequence,marker='o',ls='-')
        ax.set_xlabel(r'index $m$')
        ax.set_ylabel(r'$X_m$')
        return fig,ax

    def plot_conditional_distributions(self,m,n=0, bins=10):
        """Histogram the conditional PDF p(Xm | Xn)

        Returns a 2D histogram with Xn bins on the y-axis and Xm bins on the x-axis/axes.
        
        Parameters
        ----------
        m : int or array_like
            Index for Xm
        n : int, optional
            Index for Xn
        bins : int, optional
            Number of bins.

        Returns
        -------
        fig : figure handle
            Figure handle
        axs : axis/axes handle, shape (M,)
            Axis/Axes handle
        H_Xm_given_Xn_per_conditional : array_like, shape (N,N,M)
            Histogram of p(Xm|Xn). Will be squeezed to remove the final dimension if M=1.
        xedges_per_conditional : array_like, shape(N+1,M)
            Edges of Xn bins. Will be squeezed to remove the final dimension if M=1.
        yedges_per_conditional : array_like, shape(N+1,M)
            Edges of Xm bins. Will be squeezed to remove the final dimension if M=1.
        """
        try:
            num_conditionals = len(m)
        except TypeError:
            num_conditionals = 1
            m = [m]
        fig, axs = plt.subplots(nrows=1,ncols=num_conditionals,sharey=True,**{'figsize':(num_conditionals*4,4)})
        xedges_per_conditional = np.empty((bins+1,num_conditionals))
        yedges_per_conditional = np.empty((bins+1,num_conditionals))
        H_Xm_given_Xn_per_conditional = np.empty((bins,bins,num_conditionals))
        for i,mi in enumerate(m):
            assert mi>n
            assert self.sequence.shape[0] >= mi
            # Note the order: Xm on x-axis, Xn on y-axis
            # p(Xm, Xn) histogram and edges
            H_Xm_and_Xn,xedges,yedges = np.histogram2d(self.sequence[mi,:],self.sequence[n,:],bins=bins)
            # Histogram of p(Xn) with the same edges as above
            H_Xn, _  = np.histogram(self.sequence[n,:],bins=yedges)
            H_Xm_given_Xn =  (H_Xm_and_Xn / H_Xn).T
            #--H_Xm_given_Xn =  (H_Xm_and_Xn / H_Xn).T
            assert np.allclose(H_Xm_given_Xn.sum(axis=1),1)
            xedges_per_conditional[:,i] = xedges
            yedges_per_conditional[:,i] = yedges
            H_Xm_given_Xn_per_conditional[:,:,i] = H_Xm_given_Xn
        # Find the max and min pdf
        vmin = H_Xm_given_Xn_per_conditional.min()
        vmax = H_Xm_given_Xn_per_conditional.max()
        for i,mi in enumerate(m):
            try: ax=axs[i]
            except TypeError: ax=axs
            # Use  pcolormesh to show histogram and handle actual bin edges
            X, Y = np.meshgrid(xedges_per_conditional[:,i], yedges_per_conditional[:,i])
            cb = ax.pcolormesh(X, Y, H_Xm_given_Xn_per_conditional[:,:,i], cmap=mpl.colormaps['Reds'],vmin=vmin,vmax=vmax)
            ax.set_title(fr'$p(x_{{{mi}}} | x_{{{n}}})$')
            ax.set_xlabel(fr'$x_{{{mi}}}$')
            if ax.get_subplotspec().is_first_col:
                ax.set_ylabel(fr'$x_{{{n}}}$')
    	    
        fig.subplots_adjust(bottom=0.12, right=0.8+num_conditionals*0.025, top=0.92, wspace=0.02)
        cax = plt.axes([0.82+num_conditionals*0.025, 0.12, 0.025, 0.8])
        plt.colorbar(cb,cax=cax)
        cax.set_ylabel('pdf')
        return fig, axs, H_Xm_given_Xn_per_conditional.squeeze(),xedges_per_conditional.squeeze(),yedges_per_conditional.squeeze()

    #####################################
    # Abstract methods 
    #####################################
    
    @abstractmethod
    def start(self,random_state):
        """Return the initial value for a sequence.

        Parameters
        ----------
        random_state : RandomState
            RandomState that should be used to sample the first random variable

        Returns
        -------
        float
            The inital value to use
        """
        raise NotImplementedError



    @abstractmethod
    def update(self,random_state, history):
        """Return the next value in a sequence.

            Parameters
        ----------
        random_state : RandomState
            RandomState that should be used to sample the first random variable

        history : ndarray
            Array with previous values in the sequence

        Returns
        -------
        float
            The next value in the sequence
        """
        raise NotImplementedError
