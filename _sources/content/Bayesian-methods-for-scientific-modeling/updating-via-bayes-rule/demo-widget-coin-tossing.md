(demo:WidgetCoinTossing)=
# Demo: Widgetized coin tossing

In this section we consider an interactive version of the problem of estimating the probability that a particular coin will come up heads on any given toss, $p_H$, based on data as to how many heads (and tails) it produces in $N$ tosses. The tosses are assumed to be independent. (This example is gratefully adapted from the similar example in Sivia's book.) 

The data $D$ will then be the number of heads $H$ obtained in $N$ trials. The probability of obtaining a particular number of heads will be a function of $p_H$. This is the likelihood piece of Bayes' theorem.  Note that the *outcome* is discrete (either heads or tails), and the number of heads obtained in $N$ trials is an integer, but $p_H$ can be any real number $0 \leq p_H \leq 1$, and all our output pdfs are continuous functions of $p_H$ in the interval $0 < p_H < 1$. 

Meanwhile we can represent different prior knowledge and/or beliefs about $p_H$ in the prior, i.e., ${\rm p}(p_H|I)$. $I$ could be information regarding the character of the coin flipper, it could be based on a previous experiment (we managed to get hold of the coin and flip it a few times before hand!), or it could be an "ignorance prior", the formulation of which we will come back to later in the book. 

## Bayesian updating 

One of the key points of this exercise, is that with each flip of the coin we acquire more information on the value of $p_H$. The logical thing to do is to update the state of our belief, our pdf for $\mathrm{p}(p_H|\mbox{no. tosses, no. heads},I)$ each time the number of coin tosses is incremented by 1. The pdf will tend to get narrower as we acquire more data, i.e., our state of knowledge of $p_H$ becomes more definite. 

Note that in what follows we exploit the fungibility of mathematical symbols to let $I$ stand for different things at different stages of the coin tossing experiment. If we are going to "update" after every coin toss then $D$ is just the result of the $N$th coin toss and $I$ is what we know about the coin after $N-1$ coin tosses.

### User-interface for coin-flipping 

Take a look at the information under the `Help` tab to find out about what the controls do, what the priors are, etc. 

**Widget user interface features**:
   * tabs to control parameters or look at documentation
   * set the true $p_H$ by the slider
   * press "Next" to flip "jump" # of times
   * plot shows updating from three different initial prior pdfs

```{raw} html
<iframe src="../../../_static/demo-bayesian-coin-tossing-html5.html"
    width="100%"
    height="900"
    style="border: none;"
    scrolling="no">
</iframe>
