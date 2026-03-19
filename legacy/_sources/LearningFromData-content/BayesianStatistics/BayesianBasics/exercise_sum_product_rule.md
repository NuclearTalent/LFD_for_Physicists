(exercise:CheckingSumProduct)=
# Exercise: Checking the sum and product rules

Goal: Check using a very simple example that the Bayesian rules are consistent with standard probabilities based on frequencies.  Also reinforce notation and vocabulary.

## Reference: Bayesian rules of probability 

Notation: $\prob(x \mid I)$ is the probability  of $x$ being true
given information $I$ (we do not give the generalizations to pdfs here).

1. **Sum rule:** If set $\{x_i\}$ is exhaustive and exclusive, 
  
  $$ 
  \sum_i \prob(x_i  \mid  I) = 1   
  $$ 
  
  * cf. complete and orthonormal 
  * implies *marginalization* (cf. inserting complete set of states or integrating out variables - but be careful!)
    
  $$
   \prob(x \mid  I) = \sum_j \prob(x,y_j \mid I) 
  $$
   
  
2. **Product rule:** expanding a joint probability of $x$ and $y$  

  $$
         { \prob(x,y \mid I) = \prob(x \mid y,I)\,\prob(y \mid I)
              = \prob(y \mid x,I)\,\prob(x \mid I)}
  $$

  * If $x$ and $y$ are <em>mutually independent</em>:  $\prob(x \mid y,I) = \prob(x \mid I)$, then  
      
  $$
       \prob(x,y \mid I) \longrightarrow \prob(x \mid I)\,\prob(y \mid I)
  $$
    
  * Rearranging the second equality yields <em> Bayes' Rule (or Theorem)</em>
    
   $$
      \color{blue}{\prob(x  \mid y,I) = \frac{\prob(y \mid x,I)\, 
       \prob(x \mid I)}{\prob(y \mid I)}}
   $$

<!--See <a href="https://www.amazon.com/Algebra-Probable-Inference-Richard-Cox/dp/080186982X/ref=sr_1_1?s=books&ie=UTF8&qid=1538835666&sr=1-1">Cox</a> for the proof.-->


## Answer all the questions 

<!--Check answers with your neighbors. Ask for help if you get stuck or are unsure.-->

|     TABLE 1     | Blue         | Brown         |  Total        |
| :-------------: | :----------: | :-----------: | :-----------: |
|  **Tall**           | 1            | 17            | 18            |
| **Short**           | 37           | 20            | 57            |
| **Total**           | 38           | 37            | 75            |

|     TABLE 2     | Blue         | Brown         |  Total        |
| :-------------: | :----------: | :-----------: | :-----------: |
|  **Tall**           |      &nbsp;    |   &nbsp;        |   &nbsp;      |
| **Short**           |      &nbsp;    |   &nbsp;        |   &nbsp;      |
| **Total**           |      &nbsp;    |   &nbsp;        |   &nbsp;      |

::::{admonition} Question 1
:class: my-checkpoint
Table 1 shows the number of blue- or brown-eyed and tall or short individuals in a population of 75.
*(a) Fill in the blanks in Table 2 with probabilities (in decimals with three places, not fractions) based on the usual "frequentist" interpretations of probability* (which would say that the probability of randomly drawing an ace from a deck of cards is 4/52 = 1/13). 
<br> *(b) Put x's in any row and/or column that illustrates marginalization and y's for entries illustrating the sum rule.*

:::{admonition} Hint (a)
:class: dropdown, my-hint
**How many students are tall and blue-eyed? Just 1. There are 75 total students, so the probability is $1/75 \approx 0.013$, which goes in the first box.**
:::

:::{admonition} Answer (a)
:class: dropdown, my-answer 

|     TABLE 2     | Blue         | Brown         |  Total        |
| :-------------: | :----------: | :-----------: | :-----------: |
|  **Tall**           |      0.013    |   0.227        |   0.240       |
| **Short**           |      0.493    |   0.267        |   0.760       |
| **Total**           |      0.506    |   0.494        |   1.000       |
:::

:::{admonition} Hint (b)
:class: dropdown, my-hint
**Marginalization is $\prob(x \mid  I) = \sum_j \prob(x,y_j \mid I)$, where in this case one possibility is $x$ is "Tall" while $y_1$ is "Blue" and $y_2$ is "Brown". So $0.240 \overset{?}{=} 0.013 + 0.227$ $\Longrightarrow$ works!**
:::

:::{admonition} Answer (b)
:class: dropdown, my-answer 

|     TABLE 2     | Blue         | Brown         |  Total        |
| :-------------: | :----------: | :-----------: | :-----------: |
|  **Tall**           |      0.013    |   0.227        |   0.240 x      |
| **Short**           |      0.493    |   0.267        |   0.760 x      |
| **Total**           |      0.506 x  |   0.494 x      |   1.000 y      |

**The third (last) column and the third (last) row each illustrate marginalization (they are totals in the margin, get it?), while the grand total entry illustrates the sum rule.**

:::
::::


::::{admonition} Question 2
:class: my-checkpoint
*(a) What is $\prob(short, blue)$? Is this a joint or conditional probability? <br> (b) What is $\prob(blue)$? <br> \(c\) From the product rule, what is $\prob(short | blue)$?  Can you read this result directly from the table?*

:::{admonition} Answer (a) 
:class: dropdown, my-answer
**$\prob(short,blue) = 0.493\,$.  This is a joint probability.**
:::

:::{admonition} Answer (b) 
:class: dropdown, my-answer
**$\prob(blue) = 0.506\,$.  Note that this is from the Total row.**
:::

:::{admonition} Answer \(c\) 
:class: dropdown, my-answer
**The product rule says $\ \ \prob(short, blue) = \prob(short|blue)\, \prob(blue)\ $, so $\prob(short|blue) = 0.493/0.506 = 0.974$.  This number does not appear anywhere in the table.** 
:::
::::

::::{admonition} Question 3
:class: my-checkpoint
*Apply Bayes' theorem to find $\prob(blue | short)$ from your answers to the last part.*
:::{admonition} Answer 
:class: dropdown, my-answer
**Bayes' theorem says**

$$
p(blue|short) = \frac{p(short|blue)\, p(blue)}{p(short)} = \frac{(0.974)(0.506)}{0.760} = 0.648
$$

**Be careful not to confuse this with the box for blue *and* short, which would give $0.493$.  We *can* also find it from the table by using the product rule $\ \ p(blue|short) = p(blue,short)/p(short) = 0.493/0.760 = 0.648$.** 
:::
::::

::::{admonition} Question 4
:class: my-checkpoint
*What rule does the second row (the one starting with "Short") illustrate?  Write it out in $\prob(\cdot)$ notation.* 
:::{admonition} Answer 
:class: dropdown, my-answer
**The second row illustrates marginalization: $\ \ p(short,blue) + p(short,brown) = p(short)$.** 
:::
::::

::::{admonition} Question 5
:class: my-checkpoint
*Are the probabilities of being tall and having brown eyes mutually independent?  Why or why not?*
:::{admonition} Hint
:class: dropdown, my-hint
**If the probabilities of being tall and brown *were* independent, what would the joint probability be in terms of the individual probabilities?**
:::
:::{admonition} Answer 
:class: dropdown, my-answer
**We can test for mutual independence by seeing whether the probability of tall and brown is the product of the individual probability of being tall multiplied by the individual probability of having brown eyes:**

$$ p(tall,brown) = 0.227 \neq p(tall)\times p(brown) = 0.240 \times 0.494$$

**so they are not independent**.
 
:::
::::

