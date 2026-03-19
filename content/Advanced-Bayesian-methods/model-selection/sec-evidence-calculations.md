# Evidence calculations
The actual computation of Bayesian evidences can be a challenging task. Recall that we often have knowledge of the posterior distribution only through sampling. In many cases, the simple Laplace method can be used to compute the evidence approximately, while in other cases we have to rely on special sampling algorithms such as nested sampling or parallel tempering with thermodynamic integration.

## Laplace's method
The idea behind Laplace's method is simple, namely to use the Taylor expansion of a function around its peak to construct a Gaussian approximation which can be easily integrated. Let us consider an unnormalized density $P^*(\theta)$ that has a peak at a point $\theta_0$. 
We are interested in the evidence, $Z_P$, which is given by the integral

\begin{equation}
Z_P = \int P^*(\theta) d^K\theta,
\end{equation} 

where we consider the general case in which $\theta$ is a $K$-dimensional vector of parameters. 

We Taylor-expand the logarithm $\log P^*$ around the peak:

\begin{equation}
\log P^*(\theta) = \log P^*(\theta_0) - \frac{1}{2} (\theta - \theta_0)^T \Sigma^{-1} (\theta - \theta_0) + \ldots,
\end{equation}

where $\Sigma^{-1} \equiv H$ is the (Hessian) matrix of second derivatives at the maximum

\begin{equation}
H_{ij} = - \left. \frac{\partial^2}{\partial \theta_i \partial \theta_j}  \log P^*(\theta)\right|_{\theta=\theta_0}.
\end{equation}

By truncating the Taylor expansion at the second order we find that $P^*(\theta)$
is approximated by an unnormalized Gaussian, 

\begin{equation}
P^*(\theta) \approx P^*(\theta_0) \exp \left[ - \frac{1}{2}(\theta - \theta_0)^T \Sigma^{-1} (\theta - \theta_0) \right].
\end{equation}

The integral of this Gaussian is given by $P^*(\theta_0)$ times (the inverse of) its normalization constant. Thus we approximate $Z_P$ by

\begin{equation}
Z_P \approx P^*(\theta_0) \sqrt{\frac{(2\pi)^K}{\det\Sigma^{-1}}}.
\end{equation}

Predictions can then be made using this approximation. Physicists also call this widely-used approximation the saddle-point approximation.

Note, in particular, that if we consider a chi-squared likelihood: $P^*(\theta) = \mathcal{L}(D|\theta) = \exp \left( -\frac{1}{2} \chi^2(\theta)\right)$, then we get

\begin{equation}
Z_P \approx \exp \left( -\frac{1}{2} \chi^2(\theta_0)\right) \sqrt{\frac{(4\pi)^K}{\det\Sigma^{-1}}},
\end{equation}

where there is a factor $2^{K/2}$ that comes from the extra factor $1/2$ multiplying the covariance matrix $\Sigma^{-1}$ and therefore appearing in all $K$ eigenvalues.

Note that the Laplace approximation is basis-dependent: if $\theta$ is transformed to a nonlinear function $u(\theta)$ and the density is transformed to $P(u) = P(\theta) |d\theta/du|$ then in general the approximate normalizing constants $Z_Q$ will be different. This can be viewed as a defect&mdash;since the true value $Z_P$ is basis-independent in this approximation&mdash;or an opportunity, because we can hunt for a choice of basis in which the Laplace approximation is most accurate.

## Normalization of a multivariate Gaussian
The fact that the normalizing constant of a Gaussian is given by 

\begin{equation}
\int d^K\theta \exp \left[ - \frac{1}{2}\theta^T \Sigma^{-1} \theta \right] = \sqrt{\frac{(2\pi)^K}{\det\Sigma^{-1}}},
\end{equation}

can be proved by making an orthogonal transformation into the basis $u$ in which $\Sigma$ is transformed into a diagonal matrix of eigenvalues $\lambda_i$. The integral then separates into a product of one-dimensional integrals, each of the form

\begin{equation}
\int du_i \exp \left[ -\frac{1}{2} \lambda_i u_i^2 \right] = \sqrt{\frac{2\pi}{\lambda_i}}
\end{equation}

The product of the eigenvalues $\lambda_i$ is the determinant of $\Sigma^{-1}$.

## Correlations
In the "fitting a straight-line" example you should find that the joint pdf for the slope and the intercept $[m, b]$ corresponds to a slanted ellipse. That result implies that the model parameters are (anti) **correlated**.

* *Try to understand the correlation that you find in this example.*

Let us explore correlations by studying the behavior of a bivariate pdf near the maximum where we employ the Laplace approximation (neglecting terms beyond the quadratic one in a Taylor expansion). We start by considering two independent parameters $x$ and $y$, before studying the dependent case.

### Two independent parameters

Independence implies that $p(x,y) = p_x(x) p_y(y)$. We will again consider the log-pdf $L(x,y) = \log\left( p(x,y) \right)$ which will then be

\begin{equation}
L(x,y) = L_x(x) + L_y(y).
\end{equation}

At the mode we will have $\partial p / \partial x = \partial p_x / \partial x = \partial L_x / \partial x = 0$, and similarly $\partial L_y / \partial y = 0$.

The second derivatives will be

\begin{equation}
A \equiv \left. \frac{\partial^2 L_x}{\partial x^2} \right|_{x=x_0} < 0, \quad
B \equiv \left. \frac{\partial^2 L_y}{\partial y^2} \right|_{y=y_0} < 0, \quad
C \equiv \left. \frac{\partial L(x,y)}{\partial x \partial y} \right|_{x=x_0,y=y_0} = 0.
\end{equation}

such that our approximated (log) pdf near the mode will be

\begin{equation}
L(x,y) = L(x_0, y_0) - \frac{1}{2} |A| (x-x_0)^2 - \frac{1}{2} |B| (y-y_0)^2.
\end{equation}

We could visualize this bivariate pdf by plotting iso-probability contours. Or, equivalently, iso-log-probability contours which correspond to

\begin{equation}
|A| (x-x_0)^2 + |B| (y-y_0)^2 = \mathrm{constant}.
\end{equation}

This you should recognize as the equation for an ellipse with its center in $(x_0, y_0)$, the principal axes corresponding to the $x$ and $y$ directions, and with the width and height parameters $\sigma_x = 1/\sqrt{|A|}$ and $\sigma_y = 1/\sqrt{|B|}$, respectively.

### Two dependent parameters

For two dependent parameters we cannot separate $p(x,y)$ into a product of one-dimensional pdf:s. Instead, the Taylor expansion for the bivariate log-pdf $L(x,y)$ around the mode $(x_0,y_0)$ gives

\begin{equation}
L(x,y) \approx L(x_0,y_0) + \frac{1}{2} \begin{pmatrix} x-x_0 & y-y_0 \end{pmatrix}
H
\begin{pmatrix} x-x_0 \\ y-y_0 \end{pmatrix},
\end{equation}

where $H$ is the symmetric Hessian matrix

\begin{equation}
\begin{pmatrix}
A & C \\ C & B
\end{pmatrix}, 
\end{equation}

with elements

\begin{equation}
A = \left. \frac{\partial^2 L}{\partial x^2} \right|_{x_0,y_0} < 0, \quad
B = \left. \frac{\partial^2 L}{\partial y^2} \right|_{x_0,y_0} < 0, \quad
C = \left. \frac{\partial^2 L}{\partial x \partial y} \right|_{x_0,y_0} \neq 0.
\end{equation}

* So in this quadratic approximation the contour is an ellipse centered at $(x_0,y_0)$ with orientation and eccentricity determined by $A,B,C$.
* The principal axes are found from the eigenvectors of $H$.
* Depending on the skewness of the ellipse, the parameters are either (i) not correlated ($C=0$), (ii) correlated, or (iii) anti-correlated.
* Take a minute to consider what that implies.

Let us be explicit. The Hessian can be diagonalized (we will also change sign)

\begin{equation}
-H = U \begin{pmatrix} a & 0 \\ 0 & b \end{pmatrix} U^{-1},
\end{equation}

where $a$, $b$ are the (positive) eigenvalues of $-H$, and $U = \begin{pmatrix} a_x & b_x \\ a_y & b_y \end{pmatrix}$ is constructed from the eigenvectors. Defining a new set of translated and linearly combined parameters

\begin{equation}
x' = a_x (x - x_0) + a_y (y - y_0) \\
y' = b_x (x - x_0) + b_y (y - y_0) 
\end{equation}

we find that the log-pdf in the new coordinates becomes

\begin{equation}
\begin{gathered}
L(x',y') &= L(0,0) - \frac{1}{2} \begin{pmatrix} x' & y' \end{pmatrix}
\begin{pmatrix} a & 0 \\ 0 & b \end{pmatrix}
\begin{pmatrix} x' \\ y' \end{pmatrix} \\
&= L(0, 0) - \frac{1}{2} a (x')^2 - \frac{1}{2} b (y')^2.
\end{gathered}
\end{equation}

::::{admonition} Checkpoint question
:class: my-checkpoint
What has been achieved by this change of variables?
:::{admonition} Answer
:class: dropdown, my-answer 
The joint pdf now factorizes, which implies that the transformed variables are independent.
:::
::::

