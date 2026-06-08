---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
  name: python3
---

(sec:SVD)=
# Singular value decomposition (SVD)

A good reference for SVD is [A Singularly Valuable Decomposition: The SVD of a Matrix](http://www.math.kent.edu/~reichel/courses/intr.num.comp.1/fall11/lecture7/svd.pdf).


Some parts of this section were adapted from [Computational-statistics-with-Python.ipynb](https://github.com/cliburn/Computational-statistics-with-Python), which is from a course taught at Duke University.  

## Linear algebra manipulations

The goal here is to practice some linear algebra manipulations by hand and with Python, and to gain some experience and intuition with the Singular Value Decomposition (SVD).

### Manipulations using the index form of matrices

:::{admonition} Reminder of linear algebra using the index form 
:class: note

Recall that

$$
  (AB)^\intercal = B^\intercal A^\intercal
  \quad\mbox{and}\quad
 (A^\intercal)_{ji} = A_{ij}
$$

$$
  \chi^2 = [Y - A\thetavec]^\intercal\, \Sigmavec^{-1}\, [Y - A\thetavec] =
  (Y_i - A_{ij}\thetavec_j)(\Sigma^{-1})_{ii'}(Y_{i'}- A_{i'j'}\thetavec_{j'}) ,
$$

where $i,i'$ run from $1$ to $N$ and $j,j'$ run from one to $p$, where the highest power term is $x^{p-1}$. 
* Summed over $i,i',j,j'$ because they each appear (exactly) twice.
* $(\Sigma^{-1})_{ii'} \neq (\Sigma_{i,i'})^{-1}$
* Be sure you understand the indices on the leftmost term, remembering that the matrix expression has this term transposed.
* We know $\chi^2$ is a scalar because there are no free indices.

:::

::::{admonition} Checkpoint Question
:class: my-checkpoint
Prove that the Maximum Likelihood Estimate (MLE) for $\chi^2$ defined by 

$$
\chi^2 = (\Yvec - \Amat\thetavec)^{\mathbf{\top}} \Sigmamat^{-1} (\Yvec - \Amat\thetavec)
$$

is 

$$
\thetavec_{\mathrm{MLE}} = (\AmatT \Sigmamat^{-1} \Amat)^{-1} (\AmatT \Sigmamat^{-1} \Yvec)  \;.
$$

Here $\thetavec$ is a $m\times 1$ matrix of parameters (i.e., there are $m$ parameters), $\Sigmamat$ is the $m\times m$ covariance matrix, $\Yvec$ is a $N\times 1$ matrix of observations (data), and $\Amat$ is an $N\times m$ matrix 

$$
\Amat = 
\left(
\begin{array}{cccc}
   1  & x_1  & x_1^2 & \cdots \\
   1  & x_2  & x_2^2 & \cdots \\
   \vdots & \vdots & \vdots &\cdots \\
   1  & x_N  & x_N^2 & \cdots
\end{array}
\right)
$$

where $N$ is the number of observations.  The idea is to do this with explicit indices for vectors and matrices, using the Einstein summation convention.  
:::{admonition} Hint
:class: dropdown, my-hint 
A suggested approach:
* Write $\chi^2$ in indices: $\chi^2 = (Y_i - A_{ij}\theta_j)\Sigma^{-1}_{ii'}(Y_{i'}- A_{i'j'}\theta_{j'})$, where summations over repeated indices are implied (be careful of transposes and using enough independent indices).  *How do we see that $\chi^2$ is a scalar?*
* Find $\partial\chi^2/\partial \theta_k = 0$ for all $k$, using $\partial\theta_j/\partial\theta_k = \delta_{jk}$. Isolate the terms with one component of $\thetavec$ from those with none.
* You should get the matrix equation $ (\AmatT \Sigmamat^{-1} \Yvec) = (\AmatT \Sigmamat^{-1} \Amat)\thetavec$. At this point you can directly solve for $\thetavec$. *Why can you do this now?*
:::
:::{admonition} Answer
:class: dropdown, my-answer
We find the MLE from $\partial\chi^2/\partial\thetavec_k = 0$ for $k = 1,\ldots p$. 

$$\begin{aligned}
 \left.\frac{\partial\chi^2}{\partial\thetavec_k}\right|_    {\thetavec=\thetavechat}
 &= -A_{ij}\delta_{jk}(\Sigma^{-1})_{i,i'}(Y_{i'} - A_    {i'j'}\thetavechat_{j'}) + 
 (Y_{i} - A_{ij}\thetavechat_{j})(\Sigma^{-1})_{i,i'}(-A_    {i'j'}\delta_{j'k}) = 0
\end{aligned}$$

Isolate the $\thetavec$ terms on one side and show the doubled terms are equal:

$$
 A_{ik}(\Sigmavec^{-1})_{i,i'}Y_{i'}
 + Y_i (\Sigmavec^{-1})_{i,i'} A_{i'k}
 =
 A_{ik}(\Sigmavec^{-1})_{i,i'}A_{i'j'}\thetavechat_{j'}
 + A_{ij}\thetavechat_{j}(\Sigmavec^{-1})_{i,i'}A_{i'k}
$$   

* In the second term on the left, switch $i\leftrightarrow i'$ and use $(\Sigmavec^{-1})_{i',i} = (\Sigmavec^{-1})_{i,i'}$ because it is symmetric. This is then the same as the first term.
* In the first term on the right, we switch $j\leftrightarrow j'$ and use the symmetry of $\Sigmavec$ again to show the two terms are the same. 

Writing $A_{ik} = (A^\intercal)_{ki}$, we get
    
$$\begin{aligned}
 2(A^\intercal)_{ki} (\Sigmavec^{-1})_{i,i'} Y_i
  = 2 (A^{\intercal})_{ki} (\Sigmavec^{-1})_{i,i'} A_    {i'j}\thetavechat_j
\end{aligned}$$

or, removing the indices,

$$
  (A^{\intercal}\Sigmavec^{-1} Y) = (A^{\intercal}\Sigmavec^{-1}A)    \thetavechat
$$

and then inverting (which is possible because the expression in parentheses on the right is a square, invertible matrix), we finally obtain:

$$
  \thetavechat = [A^\intercal \Sigmavec^{-1} A]^{-1}
     [A^\intercal \Sigmavec^{-1} Y] .
$$

Q.E.D.
:::
::::



## SVD basics

Note: we will used the "reduced SVD" here, for which the matrix of singular values is square. The formal discussion of the SVD usually works with the "full SVD", the "reduced SVD" is more typically used in practice. 

A singular value decomposition (SVD) decomposes a matrix $A$ into three other matrices (we'll skip the boldface font here):

$$
A = U S V^\top
$$

where (take $m > n$ for now)
* $A$ is an $m\times n$ matrix;
* $U$ is an $m\times n$ (semi)orthogonal matrix;
* $S$ is an $n\times n$ diagonal matrix;
* $V$ is an $n\times n$ orthogonal matrix.

Comments:
* The `scipy.linalg` function `svd` has a Boolean argument `full_matrices`.  If `False`, it returns the decomposition above with matrix dimensions as stated, which is the "reduced SVD".  If `True`, then $U$ is $m\times m$, $S$ is $m \times n$, and $V$ is $n\times n$.  We will use the `full_matrices = False` form here.  *Can you see why this is ok?*
* Note that semi-orthogonal means that $U^\top U = I_{n\times n}$ and orthogonal means $V V^\top = V^\top V = I_{n\times n}$.  
* In index form, the decomposition of $A$ is $A_{ij} = U_{ik} S_k V_{jk}$, where the diagonal matrix elements of $S$ are 
$S_k$ (*make sure you agree*).
* These diagonal elements of $S$, namely the $S_k$, are known as **singular values**.  They are ordinarily arranged from largest to smallest.
* $A A^\top = U S^2 U^\top$, which implies (a) $A A^\top U = U S^2$.
* $A^\top A = V S^2 V^\top$, which implies (b) $A^\top A V = V S^2$.
* If $m > n$, we can diagonalize $A^\top A$ to find $S^2$ and $V$ and then find $U = A V S^{-1}$.  If $m < n$ we switch the roles of $U$ and $V$.


::::{admonition} Checkpoint Tasks
:class: my-checkpoint
1. Verify that these dimensions are compatible with the decomposition of $A$.*  
1. *Show from equations (a) and (b) that $U$ is semi-orthogonal and $V$ is orthogonal and that the eigenvalues, $\{S_i^2\}$, are all positive.*
1. *Show that if $m < n$ there will be at most $m$ non-zero singular values.* 
1. *Show that the eigenvalues from equations (a) and (b) must be the same.*

:::{admonition} Answers
:class: dropdown, my-answer
[to be filled in]
:::
::::


A key feature of the SVD for us here is that the sum of the squares of the singular values equals the total variance in $A$, i.e., the sum of squares of all matrix elements (squared Frobenius norm). Thus the size of each says how much of the total variance is accounted for by each singular vector.  We can create a truncated SVD containing a percentage (e.g., 99%) of the variance:

$$
  A_{ij} \approx \sum_{k=1}^{p} U_{ik} S_k V_{jk}
$$

where $p < n$ is the number of singular values included. Typically this is not a large number.

:::{admonition} Diagonalization of symmetric matrix
:class: note

If $A$ is a symmetric, real $n \times n$ matrix, then we *diagonalize* it by finding an orthogonal matrix $V$ and a diagonal matrix $D$ such that $A = V D V^\intercal$.
* The diagonal elements of $D$ are the eigenvalues of $A$.
* The *columns* of $V$ are the eigenvectors of $A$. They are *orthonormal*. (Can you prove this?)
* Following Kalman, to compare to the singular value decomposition of $A$, we might call this the *eigenvalue decomposition* (EVD) of $A$.
:::



## Applications of SVD




### Solving matrix equations with SVD

We can solve for $\mathbf{x}$:

$$\begin{aligned}
  A \mathbf{x} &= b \\
  \mathbf{x} &= V S^{-1} U^\top b
\end{aligned}$$

or $x_i = \sum_j \frac{V_{ij}}{S_j} \sum_k U_{kj} b_k$.  The value of this solution method is when we have an ill-conditioned matrix, meaning that the smallest eigenvalues are zero or close to zero.  We can throw away the corresponding components and all is well! 

:::{admonition} Ill-conditioned matrices
:class: note
It is problematic to sold matrix equations with *ill-conditioned matrices*, which means that the smallest singular value is zero or close to zero. (If zero, then the matrix is *singular*.)
* The *condition number* of a matrix is the ratio of the largest to the smallest singular value.
* If solving $Ax = h$ $\Lra$ $x = A^{-1}h$, then an error in $h$ is magnified by the condition number to give the error in $x$.
* So finite precision in $b$ leads to nonsense for $x$ if the the condition number is larger than the inverse of the machine or calculational precision. If the condition number $\kappa(A) = 10^k$, then up to $k$ digits of accuracy is lost (roughly).
:::

Comments:
- If we have a non-square matrix, the SVD still works. If $m\times n$ with $m > n$, then only $n$ singular values.
- If $m < n$, then only $m$ singular values.
- This is like solving  

  $$A^\top A \mathbf{x} = A^\top b$$

  which is called the *normal equation*.  It produces the solution to $\mathbf{x}$ that is closest to the origin, or

  $$
    \min_{\mathbf{x}} |A\mathbf x - b| \;.
  $$

**Task:** *prove these results (work backwards from the last equation as a least-squares minimization)*.




### Data reduction

For machine learning (ML), there might be several hundred variables but the algorithms are made for a few dozen.  We can use SVD in ML for variable reduction.  This is also the connection to sloppy physics models.  In general, our matrix $A$ can be closely approximated by only keeping the largest of the singular values.  We'll see that visually below using images.




### Covariance, PCA, and SVD
* Consider the covariance matrix and find its eigenvalues and eigenvectors. Since the covariance matrix is symmetric and positive, its eigenvalues are the same as the singular values. ``Center'' the data first (subtract the mean so that you deal with data having mean zero).
* PCA means to rank these. This is typically done *via* SVD (which is better numerically).
* Then one uses fewer singular values (which are the eigenvalues if it is a symmetric, square positive matrix) $\Lra$ we have reduced the number of parameters in a model (for example).




:::{admonition} Summary of SVD
:class: note
The key feature of SVD is the decomposition of a matrix into three other matrices.
* We can do full SVD or reduced SVD. The former is usually the starting point but the latter is used in practice.

* Reduced form is $ A = U S V^\intercal$, with $S$ *diagonal*. 
* $A$ is an $m\times n$ matrix, while $U$ is $m \times n$, $S$ is $n\times n$, and $V$ is $n\times n$.

* Elements of $S$, names $S_{kk'} \equiv S_k \delta_{kk'}$  are *singular values*. For a square symmetric matrix $A$, they would be the absolute values of the eigenvalues.

* Key feature:

$$
  A_{ij} \approx \sum_{k=1}^p U_{ik} S_k V_{jk} \ \mbox{with } p < n    
$$

is a truncated representation of $A$ with most of the content if the "dominant" $p$ vectors kept, which are identified by the largest singular values.
:::


## SVD applied to images for compression

Goal: read in a gray-scale image, which has $1066 \times 1600$ values. Using SVD, recreate the image with a relative error of less than 0.5%. Find the relative size of the compressed image as a percentage.

```{code-cell}
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
from skimage import io

#from sklearn.decomposition import PCA

img = io.imread('https://raw.githubusercontent.com/buqeye/LearningFromData/main/LectureNotes/_images/elephant.jpg', as_gray=True)
plt.imshow(img, cmap='gray');
plt.gca().set_axis_off()
print('shape of image: ', img.shape)
```

```{code-cell}
# Do the svd
U, S, Vt = la.svd(img, full_matrices=False)

# Check the shapes
U.shape, S.shape, Vt.shape

# Check that we can recreate the image
img_orig = U @ np.diag(S) @ Vt
print('recreated shape of image: ', img_orig.shape)
plt.imshow(img_orig, cmap='gray')
plt.gca().set_axis_off()
```

Here's how we can efficiently reduce the size of the matrices.  Our SVD should be sorted, so we are keeping only the largest singular values up to a point.

```{code-cell}
# Pythonic way to figure out when we've accumulated 99.5% of the result
k = np.sum(np.cumsum((S**2)/(S**2).sum()) <= 0.995)

# Let's plot the eigenvalues and mark where k is
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1,1,1)
ax.semilogy(S, color='blue', label='eigenvalues')
ax.axvline(k, color='red', label='99.5% of the variance');
ax.set_xlabel('eigenvalue number')
ax.legend()
fig.tight_layout()

```

Now keep only the most significant eigenvalues (those up to k).

```{code-cell}
img2 = U[:,:k] @ np.diag(S[:k])@ Vt[:k, :]
print('new shape of compressed image is: ',img2.shape)

plt.imshow(img2, cmap='gray')
plt.gca().set_axis_off();

```

That reproduced 99.5%. Now try 99%.

```{code-cell}
k99 = np.sum(np.cumsum((S**2)/(S**2).sum()) <= 0.99)
img99 = U[:,:k99] @ np.diag(S[:k99])@ Vt[:k99, :]

plt.imshow(img99, cmap='gray')
plt.gca().set_axis_off();
```


