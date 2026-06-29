(sec:PartIExercises:solutions)=
# Solutions

```{solution} exercise:CheckingSumProduct
:label: solution:CheckingSumProduct

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


