(exercise:MedicalExample)=
# Exercise: Standard medical example using Bayes

Goal: Use the Bayesian rules of probability to solve a familiar problem whose result can be non-intuitive.

This example illustrates how to avoid the [Base Rate Fallacy](https://en.wikipedia.org/wiki/Base_rate_fallacy).

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

Suppose there is an unknown disease (call it UD) and there is a test for it.

a. The false positive rate is 2.3%. ("False positive" means the test says you have UD, but you don't.) <br>
b. The false negative rate is 1.4%. ("False negative" means you have UD, but the test says you don't.)

Assume that 1 in 10,000 people have the disease. You are given the test and get a positive result.  Your ultimate goal is to find the probability that you actually have the disease.  We'll do it using the Bayesian rules.

We'll use the notation:

* $H$ = "you have UD"
* $\overline H$ = "you do not have UD"  
* $D$ = "you test positive for UD"
* $\overline D$ = "you test negative for UD"  



::::{admonition} Question 1
:class: my-checkpoint
*Before doing a calculation (or thinking too hard :), does your intuition tell you the probability you have the disease is high or low?*
<br>
<br>
:::{admonition} Answer 
:class: dropdown, my-answer 
**It seems like it should be high because the false positive rate is low.**
:::
::::


::::{admonition} Question 2
:class: my-checkpoint
*In the $\prob(\cdot | \cdot)$ notation, what is your ultimate goal?*
<br>
<br>
:::{admonition} Answer 
:class: dropdown, my-answer 
**You want to know if you have the disease, given that you have tested positively, therefore: $\ \ \prob(H | D)$**
:::
::::


::::{admonition} Question 3
:class: my-checkpoint
*Express the false positive rate in $\prob(\cdot | \cdot)$ notation.* \[Ask yourself first: what is to the left of the bar?\]
<br>
<br>
:::{admonition} Answer 
:class: dropdown, my-answer 
**The probability that you are trying to find is that you get a positive result on the test (so $D$ should be on the left of the bar) given that you don't actually have the disease (this is the "false" part).  So $\overline{H}$ on the right. (Again, when you talk about false positive it is about the test result, not the disease, so $D$ is on the left.) Overall with the probability we are given (derived from the rate):**  $\ \ \prob(D | \overline{H}) = 0.023$

:::
::::


::::{admonition} Question 4
:class: my-checkpoint
*Express the false negative rate in $\prob(\cdot | \cdot)$ notation. By applying the sum rule, what do you also know? (If you get stuck answering the question, do the next part first.)* 
<br>
<br>
:::{admonition} Answer 
:class: dropdown, my-answer 
**False negative is the counterpart of false positive, so the probability of $\overline{D}$ given $H$:  $\ \ \prob(\overline{D}|H) = 0.014$.  For both false negative and false positive cases, the probability is the *outcome of the test*, given additional information. You might have been fooled by the wording above: "false negative means you have UD, but the test says you don't". This might cause you to think that $H$ should be on the left. But reword it as: "false negative means that the test says you don't have UD, but you do". This makes it clearer that the probability is about the test result, not about the disease itself.**

**The sum rule says $\ \ \prob(D|H) + \prob(\overline{D}|H) = 1\ $, therefore we know: $\ \ \prob(D|H) = 0.986$ This probability being so close to one is what makes us think the probability we have the disease is high.**

:::
::::


::::{admonition} Question 5
:class: my-checkpoint
*Should $\prob(D|H) + \prob(D|\overline H) = 1$?
    Should $\prob(D|H) + \prob(\overline D |H) = 1$?
    (Hint: does the sum rule apply on the left or right of the $|$?)*
<br>
<br>
:::{admonition} Answer 
:class: dropdown, my-answer 
**$\prob(D|H) + \prob(D|\overline H) =  1.09 \neq 1\ \ $ so the first answer is no.  But the sum rule holds when summing over all possibilities on the *left* of the bar with the same statements on the right of the bar, which is not the case here.**

**The second sum *does* satisfy these conditions, so we expect the sum rule to hold and $\prob(D|H) + \prob(\overline D |H) = 1$, which we've already used.**

:::
::::


::::{admonition} Question 6
:class: my-checkpoint
*Apply Bayes' theorem to your result for your ultimate goal (don't put in numbers yet).
   Why is this a useful thing to do here?*
<br>
<br>
:::{admonition} Answer 
:class: dropdown, my-answer 
**Bayes' theorem with just the $p(\cdot|\cdot)$s:**

$$
  \prob(H|D) = \frac{\prob(D|H)\,\prob(H)}{\prob(D)}
$$

**This is useful because we know $\prob(D|H)$.  But we still need $\prob(H)$ and $\prob(D)$.**
:::
::::


::::{admonition} Question 7
:class: my-checkpoint
Let's find the other results we need.  *What is $\prob(H)$?
  What is $\prob(\overline H)$?*
<br>
<br>
:::{admonition} Answer 
:class: dropdown, my-answer 
**We are told that 1 in 10,000 people have the disease, so $\ \ \prob(H) = 10^{-4}$**

**That means by the sum rule that $\ \ \prob({\overline H}) = 1 - \prob(H) = 1 - 10^{-4}$**

:::
::::


::::{admonition} Question 8
:class: my-checkpoint
Finally, we need $\prob(D)$.  *Apply marginalization first, and then
  the product rule twice to get an expression for $\prob(D)$ in terms of quantities
  we know.*
<br>
<br>
:::{admonition} Answer 
:class: dropdown, my-answer 
**The strategy here is to observe that we know various probabilities with $D$ on the left of the bar and statements on the right side of the bar.  Can we combine them to get $\prob(D)$?**

**Marginalization: $\ \ \prob(D) = \prob(D, H) + \prob(D, \overline{H})\ \ $ (recall that these are joint probabilities, not conditional probabilities).**

**Now apply the product rule to each term: $\ \ \prob(D, H) = \prob(D|H)\, \prob(H)\ \ $ and $\ \ \prob(D,\overline{H}) = \prob(D|\overline{H})\, \prob(\overline{H})$** 

**Put it together with numbers:**

$$
\prob(D) = \prob(D|H)\, \prob(H) + \prob(D|\overline{H})\, \prob(\overline{H}) = 0.986\times 10^{-4} + 0.023\times(1 - 10^{-4}) \approx 0.023
$$

:::
::::


::::{admonition} Question 9
:class: my-checkpoint
*Now plug in numbers into Bayes' theorem and calculate the result.  What do you get?*
<br>
<br>
:::{admonition} Answer 
:class: dropdown, my-answer 
$$\prob(H|D) = \frac{0.986 \times 0.0001}{0.023} = 0.0043$$

**or about $0.43\%$, which is really low!**

**We conclude this is a terrible test!  If we imagine 10000 people taking the test, the expectation is that only one of them actually has UD, but 230 will get a positive result.  We need the false positive rate to be much smaller relative to the expected rate in the population for this to be a better test. (Of course, maybe this is just an inexpensive preliminary screening and the expensive test with the low false positive rate only needs to be performed on the 230 people.)**
:::
::::

## Follow-up questions to the medical example 


::::{admonition} Follow-up question on 2.
:class: my-checkpoint
Why is it $\prob(H|D)$ and not $\prob(H,D)$?
:::{admonition} Answer
:class: dropdown, my-answer 
Recall that $\prob(H,D) = \prob(H|D) \cdot \prob(D)$. You are generally interested in $\prob(H|D)$.
If you know $\prob(D) = 1$, then they are the same.
:::
::::

::::{admonition} Follow-up question on 5.
:class: my-checkpoint
The emphasis here is on the sum rule. Why didn't any column except Total in the sum/product rule notebook add to 1?
:::{admonition} Answer
:class: dropdown, my-answer 
Because we were looking at $\prob(\text{tall,blue}) + \prob(\text{short,blue}) \neq 1$, whereas $\prob(\text{tall}| \text{blue}) + \prob(\text{short}| \text{blue}) = 1$.
:::
::::

In general, and for question 6. in particular, we emphasize the usefulness of using Bayes' theorem to express $\prob(H|D)$ in terms of $\prob(D|H)$. 

