# Modeling: Barcelona Accidents 2010-2023

Everything is merged an combined in BarcelonaAccident2023.ipynb using also some functions scripted in functions_barcelona.py and/or functions_barcelona2.py

TARGET. I decided to try to predict if an accident has any severely injured or deaths. This is how I created a new column that I called "target". Its value is one if the accident has any deaths and/or severely injured people, 0 if there are no injuries or these are minor. The idea is to be able to create a model that anticipates what accidents might need to be  prioritized.

METRICS. Based on the fact that: it is a binary classification problem and,it is a very imbalanced dataset (97.5% of majority class).

  1. The most obvious metric to use is RECALL as we want to minimize the false negatives (predicting an accident not having deaths and/or severely injured when it actually has).
  2. I will use also AUC_ROC to evaluate the model and be able to play with the threshold, if necessary. I added accuracy because I want to make sure that it does not go below 70% to avoid the cry wolf syndrome.