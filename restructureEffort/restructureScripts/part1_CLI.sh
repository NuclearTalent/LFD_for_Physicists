# Create the new Part I directory tree
mkdir -p \
  "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Inference-and-PDFs/figs" \
  "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayesian-posteriors/figs" \
  "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Updating-via-Bayes-rule/figs" \
  "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Error-propagation/figs" \
  "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayes-in-practice/figs" \
  "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/figs"

############################################
# Part overview
git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/RootBayesianBasics.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Part-Overview_Bayesian-methods-for-scientific-modeling.md"

############################################
# Inference and PDFs (top)
git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Inferenceandpdfs_top.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Inference-and-PDFs/Inference-and-PDFs.md"

# Inference and PDFs (sections)
git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Inferenceandpdfs/sec-01-statements.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Inference-and-PDFs/sec-01-statements.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Inferenceandpdfs/sec-02-manipulating-probabilities-bayesian-rules-of-probability-as.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Inference-and-PDFs/sec-02-manipulating-probabilities-bayesian-rules-of-probability-as.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Inferenceandpdfs/sec-03-probability-density-functions.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Inference-and-PDFs/sec-03-probability-density-functions.md"

# Per your instruction: keep the original order so sec-05 comes BEFORE sec-04
git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Inferenceandpdfs/sec-04-summary.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Inference-and-PDFs/sec-05-expectation-values-and-moments.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/MoreBayesTheorem.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Inference-and-PDFs/sec-04-review-of-bayes-theorem.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/DataModelsPredictions.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Inference-and-PDFs/sec-06-data-models-predictions.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Bayesian_epistemology.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Inference-and-PDFs/sec-07-bayesian-epistemology.md"

############################################
# Bayesian posteriors
git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Posteriors.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayesian-posteriors/Bayesian-posteriors.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Exploring_pdfs.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayesian-posteriors/sec-01-demo-exploring-PDFs.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Exploring_pdfs_followups.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayesian-posteriors/sec-01-followup-exploring-PDFs.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Visualizing_correlated_gaussians.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayesian-posteriors/sec-01-demo-visualizing-correlated-gaussians.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Gaussians.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayesian-posteriors/sec-02-Gaussians-a-couple-of-frequentist-connections.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/visualization_of_CLT.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayesian-posteriors/sec-02-demo-visualization-of-the-central-limit-theorem.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianParameterEstimation/Interpreting2Dposteriors.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayesian-posteriors/sec-03-interpreting-2D-posteriors.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/chi_squared_tests.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayesian-posteriors/sec-04-demo-sum-of-normal-variables-squared.ipynb"

############################################
# Updating via Bayes' rule
git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/CoinTossing_top.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Updating-via-Bayes-rule/Updating-via-Bayes-rule.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/CoinTossing/sec-01-coin-tossing-frequentists-and-bayesaians.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Updating-via-Bayes-rule/sec-01-coin-tossing-frequentists-and-bayesians.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/CoinTossing/sec-02-when-do-priors-matter-when-don-t-they-matter.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Updating-via-Bayes-rule/sec-02-when-do-priors-matter-when-don-t-they-matter.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/CoinTossing/sec-03-computing-the-posterior-analytically.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Updating-via-Bayes-rule/sec-03-computing-the-posterior-analytically.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/CoinTossing/sec-04-degree-of-belief-credibility-intervals-vs-frequentist-1-sigm.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Updating-via-Bayes-rule/sec-04-degree-of-belief-credibility-intervals-vs-frequentist-one-sigma.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/CoinTossing/sec-05-take-aways-and-follow-up-questions-from-coin-flipping.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Updating-via-Bayes-rule/sec-05-take-aways-and-follow-up-questions-from-coin-flipping.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/demo-BayesianBasics.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Updating-via-Bayes-rule/sec-06-demo-bayesian-coin-tossing.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/Bayesian_updating_coinflip_interactive.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Updating-via-Bayes-rule/sec-07-demo-bayesian-coin-tossing-interactive.ipynb"

############################################
# Error propagation
git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/ErrorPropagation_top.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Error-propagation/Error-propagation.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/ErrorPropagation/sec-01-error-propagation-i-nuisance-parameters-and-marginalization.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Error-propagation/sec-01-error-propagation-i-nuisance-parameters-and-marginalization.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/ErrorPropagation/sec-02-error-propagation-ii-changing-variables.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Error-propagation/sec-02-error-propagation-ii-changing-variables.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/ErrorPropagation/sec-03-error-propagation-iii-a-useful-approximation.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Error-propagation/sec-03-error-propagation-iii-a-useful-approximation.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/ErrorPropagation/sec-04-solutions.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Error-propagation/sec-04-solutions.md"

############################################
# Bayes in practice
git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/UsingBayes.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayes-in-practice/Bayes-in-practice.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/BayesianAdvantages.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayes-in-practice/sec-01-advantages-of-the-bayesian-approach.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianWorkflow/BayesianWorkflow.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayes-in-practice/sec-02-bayesian-research-workflow.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianLinearRegression/BayesianLinearRegression_rjf.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayes-in-practice/sec-03-bayesian-linear-regression.md"

git mv "LearningFromData-content/ModelingOptimization/demo-ModelValidation.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Bayes-in-practice/sec-03-demo-linear-regression-and-model-validation.ipynb"

############################################
# Exercises
git mv "LearningFromData-content/BayesianStatistics/BayesianParameterEstimation/Exercises_parameter_estimation.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling.md"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/exercise_sum_product_rule.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/sec-01-checking-the-sum-and-product-rules.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianBasics/exercise_medical_example_by_Bayes.md" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/sec-02-standard-medical-example-using-Bayes.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianParameterEstimation/parameter_estimation_Gaussian_noise.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/sec-03-gaussian-mean-and-variance.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianParameterEstimation/radioactive_lighthouse_exercise.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/sec-04-radioactive-lighthouse-problem.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianParameterEstimation/amplitude_in_presence_of_background.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/sec-05-amplitude-of-a-signal-in-the-presence-of-background.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianParameterEstimation/parameter_estimation_fitting_straight_line_I.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/sec-06-fitting-a-straight-line-I.ipynb"

git mv "LearningFromData-content/BayesianStatistics/BayesianParameterEstimation/parameter_estimation_fitting_straight_line_II.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/sec-07-fitting-a-straight-line-II.ipynb"

git mv "LearningFromData-content/StochasticProcesses/BUQ/parameter_estimation_Gaussian_noise-2.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/sec-08-gaussian-noise-and-averages-II.ipynb"

git mv "LearningFromData-content/StochasticProcesses/BUQ/Assignment_extending_radioactive_lighthouse.ipynb" \
       "LearningFromData-content/Part_Bayesian-methods-for-scientific-modeling/Exercises_Bayesian-methods-for-scientific-modeling/sec-09-2D-radioactive-lighthouse-location-using-MCMC.ipynb"
