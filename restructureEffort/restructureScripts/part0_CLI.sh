# Create target directories
mkdir -p LearningFromData-content/Part_Overview/Introduction/figs

# Move files (use git mv to keep history)
git mv LearningFromData-content/Intro/About.md \
      LearningFromData-content/About.md

git mv LearningFromData-content/Intro/Invitation.md \
      LearningFromData-content/Part_Overview/Invitation.md

git mv LearningFromData-content/Intro/Introduction_top.md \
      LearningFromData-content/Part_Overview/Introduction/Introduction.md

git mv LearningFromData-content/Intro/Introduction/sec-01-physicist-s-perspective.md \
      LearningFromData-content/Part_Overview/Introduction/sec-01-physicist-s-perspective.md

git mv LearningFromData-content/Intro/Introduction/sec-02-bayesian-workflow.md \
      LearningFromData-content/Part_Overview/Introduction/sec-02-bayesian-workflow.md

git mv LearningFromData-content/Intro/Introduction/sec-03-machine-learning.md \
      LearningFromData-content/Part_Overview/Introduction/sec-03-machine-learning.md

git mv LearningFromData-content/Intro/Introduction/sec-04-virtues.md \
      LearningFromData-content/Part_Overview/Introduction/sec-04-virtues.md

# If a figs directory exists:
git mv LearningFromData-content/Intro/Introduction/figs \
      LearningFromData-content/Part_Overview/Introduction/figs
