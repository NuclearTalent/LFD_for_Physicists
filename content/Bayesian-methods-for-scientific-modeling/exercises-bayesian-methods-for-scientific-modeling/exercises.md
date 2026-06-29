(sec:PartIExercises:exercises)=
# Exercises for Part I

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


