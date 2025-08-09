<!-- !split -->
# Data bias and fairness in machine learning

Part of this lecture is based on the chapter **Ethics in machine learning** {cite}`Sumpter2021` by David Sumpter in [Machine Learning: A First Course for Engineers and Scientists](http://smlbook.org/book/sml-book-draft-latest.pdf) {cite}`Lindholm2021`. There are several guidelines for Fairness and Ethics in the context of Artificial Intelligence and Machine Learning. In particular, we refer to the [Ethics Guidelines for Trustworthy Artificial Intelligence](https://futurium.ec.europa.eu/en/european-ai-alliance/blog/ethics-guidelines-trustworthy-artificial-intelligence-piloting-assessment-list) by the High-Level Expert Group on AI set up by the European Commission.

<!-- !split -->
## Fairness and error functions

We have explained how a cost function is used for training a machine learning model, and how an error function can be used to assess its performance. The choices of these functions might appear a technical issue, but it should be understood that they might also affect the perceived fairness of the model. 

Before turning to a real-world example, let us introduce the so called confusion matrix. This tool is mainly used in the evaluation of binary classifiers, although the idea can be extended also to multiclass problems. In short, the confusion matrix separates the validation data into four groups depending on $y$ (the observation) and $\hat{y}$ (the model prediction). Here we use the labels $y=1$ for positive/presence and $y=-1$ for negative/absence.

|              | $y=-1$  | $y=1$  | total |
| :------------- | :------------- | :------------- |  :------------- | 
|  $\hat{y}=-1$  | True Negative (TN)   | False Negative (FN) | N$^*$ |
|  $\hat{y}=1$ |  False Positive (FP)   | True Positive (TP) | P$^*$ |
|  total |  N | P | n |

The entries in this table should be replaced with the actual numbers from the validation set. This matrix provides more information than just the accuracy of the model as it also reveals how it fails when it does. Note that P(N) denotes the total number of positive(negative) outputs in the data set, while P$^*$(N$^*) is the total number of positive(negative) class predictions made by the model. 

False postive predictions (FP) are also known as *Type I* errors, while false negatives (FN) are called *Type II* errors. Depending on the application, one of these types of errors is typically more serious than the other one. Consider for example a machine-learning model to diagnose a rare disease, or one that predicts whether a young offender is likely to commit future crimes, which type of error has the largest negative consequence in each situation? 

There is an extensive terminology connected with the confusion matrix. Let us just highlight a few metrics that might be relevant in different circumstances:

* The misclassification rate = (FN + FP) / n.
* The false positive rate (fall-out) = FP / N
* The false negative rate (miss rate) = FN / P
* The precision = TP / P$^*$ = TP / (TP + FP)

The fact that the choice of relevant metric depends on the problem reveals an important point: *There is no single function for measuring fairness*. In fact, as a machine-learning engineer you should not make claims that your model is fair, but rather make every effort to explain how the model performs in different aspects related to fairness.

### Example: The Compas algorithm

(from Sumpter 2021 {cite}`Sumpter2021`)

The Compas algorithm was developed by a private company, Northpointe, to help with criminal sentencing decisions. The model used logistic regression with input variables including age at first arrest, years of education, and questionnaire answers about family background, drug use, and other factors to predict an output variable as to whether the person would reoffend. Race was not included in the model. Nonetheless, when tested – as part of a a study by Julia Angwin and colleagues at Pro-Publica on an independently collected data set, the model gave different predictions for black defendants than for white. The results are reproduced below in the form of a confusion matrix for re-offending over the next two years.


|  **Black defendants**     | Did not reoffend ($y=-1$)  | Reoffended ($y=1$)  | 
| :------------- | :------------- | :------------- |  
|  Lower risk ($\hat{y}=-1$)  | $\rm{TN}=990$   | $\rm{FN}=532$ | 
|  Higher risk ($\hat{y}=1$) |  $\rm{FP}=805$  | $\rm{TP}=1369$ | 

|  **White defendants**     | Did not reoffend ($y=-1$)  | Reoffended ($y=1$)  | 
| :------------- | :------------- | :------------- |  
|  Lower risk ($\hat{y}=-1$)  | $\rm{TN}=1139$   | $\rm{FN}=461$ | 
|  Higher risk ($\hat{y}=1$) |  $\rm{FP}=349$  | $\rm{TP}=505$ | 

Angwin and her colleagues pointed out that the false positive rate for black
defendants, 805/(990 + 805) = 44.8%, is almost double that of white defendants,
349/(349 + 1 139) = 23.4%. This difference cannot be accounted for simply by
overall reoffending rates: although this is higher for black defendants (at 51.4%
arrested for another offence within two years), when compared to white defendants
(39.2%), these differences are smaller than the differences in false positive rates.
On this basis, the model is clearly unfair. The model is also unfair in terms of true
positive rate (recall). For black defendants, this is 1 369/(532 + 1369) = 72.0%
versus 505/(505 + 461) = 52.2% for white defendants. White offenders who go on
to commit crimes are more likely to be classified as lower risk.

In response to criticism about the fairness of their method, the company Northpointe countered that in terms of performance, the precision (positive predictive
value) was roughly equal for both groups: 1 369/(805 + 1369) = 63.0% for black
defendants and 505/(505 + 349) = 59.1% for white. In
this sense the model is fair, in that it has the same performance for both groups.
Moreover, Northpointe argued that it is precision which is required, by law, to be
equal for different categories. Again this is the problem we highlighted above, but
now with serious repercussions for the people this algorithm is applied to: black
people who won’t later reoffend are more likely to classified as high risk than white
people.


## Limitations of training data

Bias in data is an error that occurs when certain elements of a dataset are overweighted or overrepresented. Biased datasets don't accurately represent ML model's use case, which leads to skewed outcomes, systematic prejudice, and low accuracy.

Often, the erroneous result discriminates against a specific group or groups of people. For example, data bias reflects prejudice against age, race, culture, or sexual orientation. In a world where AI systems are increasingly used everywhere, the danger of bias lies in amplifying discrimination.

It takes a lot of training data for machine learning models to produce viable results. If you want to perform advanced operations (such as text, image, or video recognition), you need millions of data points. Poor or incomplete data as well as biased data collection & analysis methods will result in inaccurate predictions because the quality of the outputs is determined by the quality of the inputs. 

If you think data bias is the problem of recent times, it’s not. Dating back to 1988, British Medical Journal described a case from St George's Hospital Medical School.

The school developed a program that aimed to reduce the amount of work when selecting candidates for interviews. The school believed it would eliminate human error and inconsistencies. 

But the [Commission of Racial Equality found the school guilty of discrimination against women and people with non-European sounding names](https://en.wikipedia.org/wiki/Medical_School_Admissions:_Report_of_a_formal_investigation_into_St._George%27s_Hospital_Medical_School_(1988)). In fact, the program bared the bias that already existed in the system.

### Data bias types in machine learning, including examples

If you want to build a fair AI project and use data ethically, you have to know the types of data bias in machine learning to spot them before they wreck your ML model.

However, data bias in machine learning doesn’t only result from skewed data. There are far more reasons such a bias occurs. Let's take a deeper look (list from [8 types of data bias that can wreck your machine learning models](https://www.statice.ai/post/data-bias-types) by Joanna Kamińska)

```{admonition}  Systemic biases
Systemic bias occurs when certain social groups are favored and others are devalued. 

The National Institute of Standards and Technology (NIST) provides a good example of such bias in their recent special publication on managing bias in AI - the infrastructure for daily living (in most cases) isn’t adjusted to the needs of disabled people. 

The reason behind it is institutional and stems from the underrepresentation of disabled people in studies. So, the biggest problem with systemic bias is that it is stealthily hidden in the world and thus overlooked.

Another example of systemic bias comes from St George's Hospital Medical School. This type of bias results from wrong procedures and practices in an organization. Although engineers don’t want to discriminate against any group of people, the bias is already rooted in the system. 
```

```{admonition}  Automation bias
Have you ever used a digital tool that, based on artificial intelligence, suggested an action? Automation bias occurs when you take this AI-based recommendation and use it before verifying if the information was right. 

For instance, a data scientist depends on the analytics platform's suggestions to remove or modify specific data despite the recommendations worsening the quality of this data. 
```

```{admonition}  Selection bias
Randomization is the process that balances out the effects of uncontrollable factors - variables in a data set that are not specifically measured and can compromise results. In data science, selection bias occurs when you have data that aren’t properly randomized. If your dataset isn’t properly randomized, it means the sample isn’t representative - it doesn’t truly reflect the analyzed population.

For instance, when building models for healthcare exploration, a data scientist operates only on white patients. This data sample isn’t reflecting the entire population because it doesn’t take into account BIPOC (Black, Indigenous, and people of color) patients. 

This case also overlaps with racial bias – when data skews in favor of a particular group of people from specific demographics. 
```

```{admonition}  Overfitting and underfitting the data
In machine learning, overfitting occurs when a model is trained with so much data that it begins to learn from the noise and inaccurate data entries in the data set. Machine learning models have trouble predicting new data based on the training data because this noise cannot be applied to new data. 

When a machine learning model fails to capture the underlying trend of the data (because it is too simple), underfitting occurs. In this case, it indicates that the model or algorithm is not fitting the data well enough.
```

```{admonition}  Reporting Biases
A reporting bias is the inclusion of only a subset of results in an analysis, which typically only covers a small fraction of evidence. Reporting bias can take many forms. An example would be analyzing data based on studies found in citations of other studies (citation bias), excluding reports not written in the scientist's native language (language bias), or choosing studies with positive findings rather than negative findings (publication bias) & more.

As an example, a sentiment analysis model can be trained to predict whether a book review on a popular website is positive or negative. The vast majority of reviews in the training data set reflect extreme opinions (reviewers who either adored or despised a book). This was because people were less likely to review a book they did not feel strongly about. Because of this, the model is less likely to accurately predict sentiment of reviews that use more subtle language to describe a book.
```

```{admonition}  Overgeneralization Bias
When a person applies something from one event to all future events, it is overgeneralization. In the field of data science, whenever you assume that what you see in your dataset is also what would be seen in another dataset, you are overgeneralizing.
```

```{admonition}  Group Attribution Biases
Group attribution biases refer to the human tendency to assume that an individual's characteristics are always determined by the beliefs of the group, or that a group's decisions are influenced by the feelings of all its members. The group attribution bias manifests itself when you give preference to your own group (in-group bias) or when you stereotype members of groups you don't belong to (out-group bias). 

For example, engineers might be predisposed to believe that applicants who attended the same school as they did are better qualified for a job when training a résumé-screening model for software developers.
```

```{admonition}  Implicit Biases
Implicit biases occur when we make assumptions based on our personal experiences. Implicit bias manifests itself as attitudes and stereotypes we hold about others, even when we are unaware of it.

We might look for information that would support our beliefs and hypotheses and disregard information that doesn't. You may be more likely to continue testing machine learning models until you obtain results that support your hypothesis (confirmation bias).

When there is not enough data or the data is not representative, you end up with sample bias. For instance, if your training data only features male doctors, the system may conclude that all doctors are male. 

Existing stereotypes and poor measurement can creep in data at the stage of data collection. Diverse and representative datasets are crucial for machine learning. When you don't have enough original training data, which is often the case, synthetic data can be used to supplement it. 
```

## Ethics guidelines

Although there are methods to reach for fairness, the most important lesson here is *awareness*. Machine-learning engineers have a responsibility to be aware of model limitations and to describe and discuss them with users.

The [Ethics Guidelines for Trustworthy Artificial Intelligence](https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai) by the High-Level Expert Group on AI set up by the European Commission identifies ethical principles that must be respected in the development, deployment and use of AI systems: 

```{admonition} Ethical principles
- Develop, deploy and use AI systems in a way that adheres to the ethical principles of: respect for human autonomy, prevention of harm, fairness and explicability. Acknowledge and address the potential tensions between these principles.
- Pay particular attention to situations involving more vulnerable groups such as children, persons with disabilities and others that have historically been disadvantaged or are at risk of exclusion, and to situations which are characterised by asymmetries of power or information, such as between employers and workers, or between businesses and consumers.
- Acknowledge that, while bringing substantial benefits to individuals and society, AI systems also pose certain risks and may have a negative impact, including impacts which may be difficult to anticipate, identify or measure (e.g. on democracy, the rule of law and distributive justice, or on the human mind itself.) Adopt adequate measures to mitigate these risks when appropriate, and proportionately to the magnitude of the risk.
```

They also list seven requirements that AI systems should meet.

```{admonition} Requirements for AI systems
- Ensure that the development, deployment and use of AI systems meets the seven key requirements for Trustworthy AI: 
  1. human agency and oversight, 
  2. technical robustness and safety, 
  3. privacy and data governance, 
  4. transparency, 
  5. diversity, non-discrimination and fairness, 
  6. environmental and societal well-being and 
  7. accountability.
- Consider technical and non-technical methods to ensure the implementation of those requirements.
```