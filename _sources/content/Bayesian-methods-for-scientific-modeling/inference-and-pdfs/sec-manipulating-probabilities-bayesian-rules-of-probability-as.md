(sec:Inference:manipulation)=
# Manipulating probabilities: Bayesian rules of probability as principles of logic

There can be many different ways by which we attain our current state of knowledge. What we know about a particular parameter may be based on bounds on what is physically sensible (e.g., masses are positive), or on the results of a previous experiment (e.g., there have already been several measurements of Newton's gravitational constant), or we might know something based on the overall scales in the problem (e.g., baseball speeds are typically not larger than 150 mph). In a Bayesian formulation any of these pieces of knowledge can be represented as a probability. Regardless of how we arrived at our state of knowledge it is crucial that we know how to combine it with other knowledge. For that purpose we need rules that allow us to keep track of probabilities. 

A minimal set of rules for consistently keeping track of probabilities
is provided by two basic rules of probability arithmetic. These are the sum
and product rules. These rules can be derived from Kolmogorov's axioms of probability,
see [](introduction:definitions), which showed that probabilities can be incorporated into mathematics using the existing theory of measures. More generally, a proof that the Sum and Product rules follow in any consistent implementation of probabilistic reasoning is given by Cox {cite}`Cox:1961`. 

## Sum rule
If the set $\{x_i\}$ is *exhaustive* and *exclusive*

$$
   \sum_i \cprob{x_i}{I} = 1,
$$ (eq:discrete_sum_rule)

i.e., the sum of the probabilities of all possible outcomes is equal
to one. In quantum mechanics we are used to this as the outcome of
summing over a complete, orthonormal set of states, and indeed, in
that case the basis includes all possible values (it's complete), and
there is no overlap between its members (they are orthogonal). 

:::{note}
In {eq}`eq:discrete_sum_rule` we include $I$ (for "Information") generically as the quantities or statements that the probability of $x_i$ is contingent on. We use $I$ to avoid having to specify explicitly all the details, but we should remember that these probabilities (and probability densities introduced below) are always conditional on some information.
:::

## Product rule

The product rule tells us how to expand the joint probability of $x$
and $y$, i.e., 

$$  
\cprob{x,y}{I} = \cprob{x}{y, I} \cprob{y}{I} 
$$ (eq:joint_prob)

In words we say that the probability of both $x$ and $y$ occurring is
the probability that $x$ occurs, given that $y$ has occurred, times
the probability that $y$ occurs. 

Note, once again, that the given information $I$ is held fixed, i.e., it
if present on the left-hand side it appears in both probabilities on
the right-hand side. 

If $x$ and $y$ are *mutually independent*, then $\cprob{x}{y,I} = \cprob{x}{I}$ and {eq}`eq:joint_prob` reduces to 

$$
\cprob{x,y}{I} = \cprob{x}{I}  \cprob{y}{I}
$$ (eq:conditional_independence)

This is a rule you are probably (but we hesitate to quantify our
belief) familiar with. Crucially, {eq}`eq:joint_prob` does _not_
rely on the independence of the events $x$ and $y$.

:::{note}
When considering whether $x$ and $y$ are mutually independent, you can ask yourself: does knowing $y$ is true give me any information about whether $x$ is true? If yes, then we need to keep it on the right side of the bar in $\cprob{x}{y,I}$. If no, then it doesn't change the probability of $x$ whether it is there or not, so the probability of $x$ being true is the same if $y$ is omitted.
Hence $\cprob{x}{y,I} = \cprob{x}{I}$ follows.
:::


## Bayes' theorem

It is just a short step from the product rule to Bayes'
theorem. Although we wrote {eq}`eq:joint_prob` so that the
$\cprob{x}{y,I}$ appeared on the right-hand side there is no reason to
privilege $x$ over $y$. We could equally have written:

$$  
\cprob{x,y}{I} = \cprob{y}{x, I} \cprob{x}{I} 
$$ 

Equating this to the expression in {eq}`eq:joint_prob` yields **Bayes' Rule** (or Theorem):

\begin{equation}
\cprob{x}{y,I} = \frac{\cprob{y}{x,I} \cprob{x}{I}}{\cprob{y}{I}}
\end{equation}

Bayes' theorem tells us how to reverse the conditional: $\cprob{y}{x}
\Rightarrow \cprob{x}{y}$. The first thing to realize is that these two
probabilities are not the same thing.

::::{admonition} Checkpoint question
:class: my-checkpoint
Construct your own example of $\cprob{x}{y} \neq \cprob{y}{I}$
:::{admonition} Possible answers 
:class: dropdown, my-hint 
The probability that there is a cloud in the sky given that it is
raining is not the same as the probability that it's raining given
that there is a cloud in the sky. 
:::
::::


```{admonition} Ingredients of Bayes' theorem
A typical use of Bayes' theorem is to update information on a hypothesis $y$ according to new data $x$ that we obtain. In that case the various terms in the theorem have formal names. 
* The quantity on the far right, $\cprob{y}{I}$, is called the *prior* probability; it represents our state of knowledge (or ignorance) about the truth of the hypothesis $y$ before we have analysed the new data $x$.
* This is modified by additional information on $y$ through $\cprob{x}{y,I}$, the *likelihood* function, that tells us how likely it is that we measure $x$, given that $y$ is true (and $I$ is true as well). 
* The denominator $\cprob{x}{I}$ is called the *evidence*. It does not depend on the hypothesis and can be regarded as a normalization constant in many situations. 
* Together, these yield the *posterior* probability, $\cprob{y}{x,I}$, representing ourupdated state of knowledge about the hypothesis $y$ in light of the information we had before, $I$, and the additional data $x$.

In this sense, Bayes’ theorem is a mathematically rigorous statement of how probabilities should be updated in light of new information: the process of learning from data.
```


## The friends of Bayes' theorem

```{admonition} Normalization and marginalization

Given an exclusive and exhaustive list of hypotheses, $y_j$, we must have a normalization of the total probability

\begin{equation}
  \sum_j \cprob{y_j}{I} = 1,
\end{equation}

which also leads to the marginalization property


\begin{align}
      \cprob{x}{I} = \sum_j \cprob{y_j}{x,I} \cprob{x}{I}=\sum_j \cprob{x, y_j}{I} 
\end{align}

where we used the product rule in the second step.
  ```

This is a key tool in the Bayesian's arsenal: the ability to obtain the  "marginal" probability for the outcome of one variable by summing the joint probability for $x$ and $y$ over all possible outcomes $\{y_j\}$ of the second variable. This second variable
is not one we are interested in when computing the pdf $\cprob{x}{I}$, so we "marginalize over it". 

 We will use marginalization a lot! Note that the marginalization
 takes place in the presence of the conditional I, i.e., all
 probabilities involved are "given the information I". The given
 information is held fixed, while the sum of all possibilities is
 constructed.

For example, let’s imagine that there are five candidates in a presidential election; then $H_1$ could be the proposition that the first candidate will win, and so on. The probability that $A$ is true, for example that unemployment will be lower in a year’s time (given all relevant information $I$, but irrespective of whoever becomes president) is given by $\prob(A|I) = \sum_i \prob(A,H_i|I)$. The president is a nuisance variable who has been marginalized out of the calculation. 

:::{warning}
Although we alluded to the analogy between inserting a complete set
of states in quantum mechanics and marginalization above this analogy breaks down in
general. It's ok to use this as a mnemonic though.
:::

:::{note}
A rule from probability says $\prob(A \cup B) = \prob(A) + \prob(B) - \prob(A \cap B)$. (That is, to calculate the probability of the union of $A$ and $B$ we need to subtract the probability of the intersection from the sum of probabilities.) This may seem to contradict our marginalization rule. However, if $A$ and $B$ are *exclusive* (as we assume) then $\prob(A \cap B) = 0$.
:::


<!--
```{exercise} Practicing the sum and product rule with population characteristics
:label: exercise:Inferenceandpdfs:sumandproductrule

In this {ref}`exercise:CheckingSumProduct`
you go through some calculations based on the sum and product
rule. You estimate the probabilities of finding an individual in a
population with a particular characteristic (tall with brown eyes for
example) based on what you're told about the population and the usual
frequentist interpretation of probability. Then the exercise will take
you through applying the sum and product rules. 
```

```{exercise} Using Bayesian rules of probability on a standard medical problem
:label: exercise:Inferenceandpdfs:medicalexample

In this {ref}`exercise:MedicalExample` your goal is to find the probability that you actually have an unknown disease given some information about the test for it. This is a problem for which your intuition and personal probability reasoning logic is likely to fail. But Bayes leads the way to the correct answer! It is good practice in translating statements to probabilities (and distinguishing between joint and conditional probabilities). 
```
-->


```{exercise} Checking the sum and product rules
:label: exercise:CheckingSumProduct

Goal: Check using a very simple example that the Bayesian rules are consistent with standard probabilities based on frequencies.  Also reinforce notation and vocabulary.

|     TABLE 1     | Blue         | Brown         |  Total        |
| :-------------: | :----------: | :-----------: | :-----------: |
|  **Tall**           | 1            | 17            | 18            |
| **Short**           | 37           | 20            | 57            |
| **Total**           | 38           | 37            | 75            |

<br/>

|     TABLE 2     | Blue         | Brown         |  Total        |
| :-------------: | :----------: | :-----------: | :-----------: |
|  **Tall**           |      &nbsp;    |   &nbsp;        |   &nbsp;      |
| **Short**           |      &nbsp;    |   &nbsp;        |   &nbsp;      |
| **Total**           |      &nbsp;    |   &nbsp;        |   &nbsp;      |

Table 1 shows the number of blue- or brown-eyed and tall or short individuals in a population of 75.

**Question 1**

1(a) Fill in the blanks in Table 2 with probabilities (in decimals with three places, not fractions) based on the usual "frequentist" interpretations of probability* (which would say that the probability of randomly drawing an ace from a deck of cards is 4/52 = 1/13). 

1(b) Put x's in any row and/or column that illustrates marginalization and y's for entries illustrating the sum rule.

Hint 1(a)
How many students are tall and blue-eyed? Just 1. There are 75 total students, so the probability is $1/75 \approx 0.013$, which goes in the first box.

Hint 1(b)
Marginalization is $\prob(x \mid  I) = \sum_j \prob(x,y_j \mid I)$, where in this case one possibility is $x$ is "Tall" while $y_1$ is "Blue" and $y_2$ is "Brown". So $0.240 \overset{?}{=} 0.013 + 0.227$ $\Longrightarrow$ works!

**Question 2**

2(a) What is $\prob(short, blue)$? Is this a joint or conditional probability? 

2(b) What is $\prob(blue)$? 

2\(c\) From the product rule, what is $\prob(short | blue)$?  Can you read this result directly from the table?

**Question 3**

Apply Bayes' theorem to find $\prob(blue | short)$ from your answers to the last part.*

**Question 4**

What rule does the second row (the one starting with "Short") illustrate?  Write it out in $\prob(\cdot)$ notation.

**Question 5**

Are the probabilities of being tall and having brown eyes mutually independent?  Why or why not?

Hint:
If the probabilities of being tall and brown *were* independent, what would the joint probability be in terms of the individual probabilities?
```

```{exercise} Standard medical example using Bayes
:label: exercise:MedicalExample

Goal: Use the Bayesian rules of probability to solve a familiar problem whose result can be non-intuitive.

Suppose there is an unknown disease (call it UD) and there is a test for it.

a. The false positive rate is 2.3%. ("False positive" means the test says you have UD, but you don't.) <br>
b. The false negative rate is 1.4%. ("False negative" means you have UD, but the test says you don't.)

Assume that 1 in 10,000 people have the disease. You are given the test and get a positive result.  Your ultimate goal is to find the probability that you actually have the disease.  We'll do it using the Bayesian rules.

We'll use the notation:

* $H$ = "you have UD"
* $\overline H$ = "you do not have UD"  
* $D$ = "you test positive for UD"
* $\overline D$ = "you test negative for UD"  

**Question 1**
Before doing a calculation (or thinking too hard :), does your intuition tell you the probability you have the disease is high or low?


**Question 2**
In the $\prob(\cdot | \cdot)$ notation, what is your ultimate goal?

**Question 3**
Express the false positive rate in $\prob(\cdot | \cdot)$ notation. 
\[Ask yourself first: what is to the left of the bar?\]


**Question 4**
Express the false negative rate in $\prob(\cdot | \cdot)$ notation. By applying the sum rule, what do you also know? (If you get stuck answering the question, do the next part first.)

**Question 5**
Should $\prob(D|H) + \prob(D|\overline H) = 1$?
Should $\prob(D|H) + \prob(\overline D |H) = 1$?
(Hint: does the sum rule apply on the left or right of the $|$?)


**Question 6**
Apply Bayes' theorem to your result for your ultimate goal (don't put in numbers yet). Why is this a useful thing to do here?

**Question 7**
Let's find the other results we need. What is $\prob(H)$? What is $\prob(\overline H)$?

**Question 8**
Finally, we need $\prob(D)$. Apply marginalization first, and then the product rule twice to get an expression for $\prob(D)$ in terms of quantities we know.

**Question 9**
Now plug in numbers into Bayes' theorem and calculate the result.  What do you get?
```

{numref}`exercise:MedicalExample` illustrates how to avoid the [Base Rate Fallacy](https://en.wikipedia.org/wiki/Base_rate_fallacy).


::::{admonition} Follow-up question on {numref}`exercise:MedicalExample`:2.
:class: my-checkpoint
Why is it $\prob(H|D)$ and not $\prob(H,D)$?
:::{admonition} Answer
:class: dropdown, my-answer 
Recall that $\prob(H,D) = \prob(H|D) \cdot \prob(D)$. You are generally interested in $\prob(H|D)$.
If you know $\prob(D) = 1$, then they are the same.
:::
::::

::::{admonition} Follow-up question on {numref}`exercise:MedicalExample`:5.
:class: my-checkpoint
The emphasis here is on the sum rule. Why didn't any column except Total in the sum/product rule notebook add to 1?
:::{admonition} Answer
:class: dropdown, my-answer 
Because we were looking at $\prob(\text{tall,blue}) + \prob(\text{short,blue}) \neq 1$, whereas $\prob(\text{tall}| \text{blue}) + \prob(\text{short}| \text{blue}) = 1$.
:::
::::

In general, and for {numref}`exercise:MedicalExample`:6. in particular, we emphasize the usefulness of using Bayes' theorem to express $\prob(H|D)$ in terms of $\prob(D|H)$. 



## Solutions to exercises


```{solution} exercise:CheckingSumProduct
:label: solution:CheckingSumProduct
:class: dropdown

**Question 1**

(a)
|     TABLE 2     | Blue         | Brown         |  Total        |
| :-------------: | :----------: | :-----------: | :-----------: |
|  **Tall**           |      0.013    |   0.227        |   0.240       |
| **Short**           |      0.493    |   0.267        |   0.760       |
| **Total**           |      0.506    |   0.494        |   1.000       |

<br/>

(b)
|     TABLE 2     | Blue         | Brown         |  Total        |
| :-------------: | :----------: | :-----------: | :-----------: |
|  **Tall**           |      0.013    |   0.227        |   0.240 x      |
| **Short**           |      0.493    |   0.267        |   0.760 x      |
| **Total**           |      0.506 x  |   0.494 x      |   1.000 y      |

The third (last) column and the third (last) row each illustrate marginalization (they are totals in the margin, get it?), while the grand total entry illustrates the sum rule.

**Question 2**

(a) 
$\prob(short,blue) = 0.493\,$.  This is a joint probability.

(b) 
$\prob(blue) = 0.506\,$.  Note that this is from the Total row.

\(c\) 
The product rule says $\ \ \prob(short, blue) = \prob(short|blue)\, \prob(blue)\ $, so $\prob(short|blue) = 0.493/0.506 = 0.974$.  This number does not appear anywhere in the table.

**Question 3**

Bayes' theorem says

$$
p(blue|short) = \frac{p(short|blue)\, p(blue)}{p(short)} = \frac{(0.974)(0.506)}{0.760} = 0.648
$$

Be careful not to confuse this with the box for blue *and* short, which would give $0.493$.  We *can* also find it from the table by using the product rule $\ \ p(blue|short) = p(blue,short)/p(short) = 0.493/0.760 = 0.648$.

**Question 4**

The second row illustrates marginalization: $\ \ p(short,blue) + p(short,brown) = p(short)$.

**Question 5**

We can test for mutual independence by seeing whether the probability of tall and brown is the product of the individual probability of being tall multiplied by the individual probability of having brown eyes:

$$ p(tall,brown) = 0.227 \neq p(tall)\times p(brown) = 0.240 \times 0.494$$

so they are not independent.
 
```

```{solution} exercise:MedicalExample
:label: solution:MedicalExample
:class: dropdown

**Question 1**
It seems like it should be high because the false positive rate is low.

**Question 2**
You want to know if you have the disease, given that you have tested positively, therefore: $\ \ \prob(H | D)$

**Question 3**
The probability that you are trying to find is that you get a positive result on the test (so $D$ should be on the left of the bar) given that you don't actually have the disease (this is the "false" part).  So $\overline{H}$ on the right. (Again, when you talk about false positive it is about the test result, not the disease, so $D$ is on the left.) Overall with the probability we are given (derived from the rate):  
$\ \ \prob(D | \overline{H}) = 0.023$



**Question 4**
False negative is the counterpart of false positive, so the probability of $\overline{D}$ given $H$:  $\ \ \prob(\overline{D}|H) = 0.014$.  For both false negative and false positive cases, the probability is the *outcome of the test*, given additional information. You might have been fooled by the wording above: "false negative means you have UD, but the test says you don't". This might cause you to think that $H$ should be on the left. But reword it as: "false negative means that the test says you don't have UD, but you do". This makes it clearer that the probability is about the test result, not about the disease itself.

The sum rule says $\ \ \prob(D|H) + \prob(\overline{D}|H) = 1\ $, therefore we know: $\ \ \prob(D|H) = 0.986$ This probability being so close to one is what makes us think the probability we have the disease is high.


**Question 5**
$\prob(D|H) + \prob(D|\overline H) =  1.09 \neq 1\ \ $ so the first answer is no.  But the sum rule holds when summing over all possibilities on the *left* of the bar with the same statements on the right of the bar, which is not the case here.

The second sum *does* satisfy these conditions, so we expect the sum rule to hold and $\prob(D|H) + \prob(\overline D |H) = 1$, which we've already used.

**Question 6**
Bayes' theorem with just the $p(\cdot|\cdot)$s:

$$
  \prob(H|D) = \frac{\prob(D|H)\,\prob(H)}{\prob(D)}
$$

This is useful because we know $\prob(D|H)$.  But we still need $\prob(H)$ and $\prob(D)$.


**Question 7**
We are told that 1 in 10,000 people have the disease, so $\ \ \prob(H) = 10^{-4}$.

That means by the sum rule that $\ \ \prob({\overline H}) = 1 - \prob(H) = 1 - 10^{-4}$.


**Question 8**
The strategy here is to observe that we know various probabilities with $D$ on the left of the bar and statements on the right side of the bar.  Can we combine them to get $\prob(D)$?

Marginalization: $\ \ \prob(D) = \prob(D, H) + \prob(D, \overline{H})\ \ $ (recall that these are joint probabilities, not conditional probabilities).

Now apply the product rule to each term: $\ \ \prob(D, H) = \prob(D|H)\, \prob(H)\ \ $ and $\ \ \prob(D,\overline{H}) = \prob(D|\overline{H})\, \prob(\overline{H})$

Put it together with numbers:

$$
\prob(D) = \prob(D|H)\, \prob(H) + \prob(D|\overline{H})\, \prob(\overline{H}) = 0.986\times 10^{-4} + 0.023\times(1 - 10^{-4}) \approx 0.023
$$


**Question 9**
$$\prob(H|D) = \frac{0.986 \times 0.0001}{0.023} = 0.0043$$

or about $0.43\%$, which is really low!

We conclude this is a terrible test!  If we imagine 10000 people taking the test, the expectation is that only one of them actually has UD, but 230 will get a positive result.  We need the false positive rate to be much smaller relative to the expected rate in the population for this to be a better test. (Of course, maybe this is just an inexpensive preliminary screening and the expensive test with the low false positive rate only needs to be performed on the 230 people.)

```




