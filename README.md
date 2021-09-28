# BarcelonaAccidents

OBJECTIVE. Develop a model in ml that will predict when an accident has severely injured people or deaths.

DATA SOURCE: From the city of Barcelona open data server. https://opendata-ajuntament.barcelona.cat/en . The weather part is obtained from darksky API.

LIMITATIONS: Amongst other limitations more common in any given dataset, I only have the accidents in Barcelona during 2010-2020 reported by the Local Police (aka Guardia Urbana)

DATASETS:

The final dataset used in this project is the final aggregation of the following datasets:

1. Accidents. It contains the basic information of the accident like its location (street, district, neighborhood, longitude and latitude, etc) and its timeline (month, year, day, hour) and also the cause of the pedestrian, number of deaths, injured (severe and minor) and the total of people injured and the number of vehicles involved.
2. Causes. It adds the cause of the accident when it has any cause specified. In some cases, there is more than one cause (it happens quite often) I ended up selecting the least common one.
3.People. This one adds very relevant information like the age of the people involved, the role (driver, passenger, pedestrian), the gender and the vehicle they were in.
4. Types. It indicates the general description of the accident like collision, overturning, fall, crash, etc)
5. Vehicles. This one a part from adding the color, brand and model of the vehicle, also gives us the type of license that the driver holds and his/her seniority.
6. Weather. It has the weather conditions of the city of Barcelona by the hour.


Everything is merged an combined in BarcelonaAccident2020.ipynb using also some functions scripted in functions_barcelona.py and/or functions_barcelona2.py

TARGET. I decided to try to predict if an accident has any severely injured or deaths. This is how I created a new column that I called "target". Its value is one if the accident has any deaths and/or severely injured people, 0 if there are no injuries or these are minor. The idea is to be able to create a model that anticipates what accidents might need to be  prioritized.

METRICS. First of all, it is a binary classification problem. Secondly,it is a very imbalanced dataset (97.5% of majority class).

Based on this:

  1. The most obvious metric to use is RECALL as we want to minimize the false negatives (predicting an accident not having deaths and/or severely injured when it actually has).
  2. I will use also AUC_ROC to evaluate the model and be able to play with the threshold, if necessary. I added accuracy because I want to make sure that it does not go below 70% to avoid the cry wolf syndrome.
