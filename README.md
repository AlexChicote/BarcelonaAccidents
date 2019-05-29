# BarcelonaAccidents
Let's find out what we can learn about the accidents and therefore prevent them. In order to do this we will be analyzing this database.
This data set is obtained in open data Barcelona webpage and available to everybody ready to dig in. This is my modest homage to all of you, fellow Catalans!!!!!
Here we have some description:

1. Dataset contains all the accidents that the local police attended from 2010 to 2018. It does not include any accident that was not reported to thee local police (aka Guardia Urbana).
2. The information gathered is spread in different CSV:

    - Accidents. This one has all information about the accident including time, location, number of victims and deceased and he number of vehicles. It also includes a column in which it is determined if it was a pedestrian responsible for the event.
    - Causes of the accident. This one adds 'initial_street' and 'mediate_cause'. While the meaning of the first added column is unclear and will need further analysis, the second one -'mediate_cause' - indicates the reason - if any - behind the accident.
    - People. Incorporates information about the people involved like age, gender, degree of injuries, who is responsible etc
    - Types. This CSV adds a filed named 'accidents_details' and it describes the reason behind E. the accident.
    - Vehicles involved. This file adds a bunch of details about the vehicle involved from a description of it up to its model and brand name. It also includes info about the experience of the driver.
3. It has been a hard work to combine all different CSV due to different encodings and column's names. Once I have done it, I am working with the first file to analyze the data:Barcelona_accidents.
4. In this file, I basically analyze the relationship in between the number of deaths and the number of accidents. AT the same time, I introduce other factors like location, dates, etc. All this is developed in the file BarcelonaAccidentsPlotting.
5. The next step is BuildingAModel. In order to build a model, I have to define the target and, once done it and depending on it, its metrics.

TARGET. I decided to try to predict if an accident has any severely injured or deaths. This is how I created a new column that I called "victims_alert". Its value is one if the accident has any deaths and/or severely injured people, 0 if there are no injuries or these are minor. The idea is to be able to create a model that anticipates what accidents might need to be  prioritized.
I want to point out that I did also consider to include the minor injuries in the target but I finally rejected the idea. There are two reasons why: the first one is that it is not, in my opinion, that interesting (understanding that every accidents needs to be attended as fast as possible) to try to prioritize situations that are not emergencies. The second one is that in doing so I would have ended up including more (or close to) 50% of the accidents to ensure success making the model useless.
I want to mention that I also considered to have total amount of injured as a target (it would include minor injures) but I discarded it. The reason why I did this is because the number of accidents with any injured is over 90%: try to predict them making sure no one is missing is like considering them all.

METRICS. Once defined the target it is time to decide what the best metric is. First of all, it is a binary classification problem. Secondly, and just to be clear, I want to explain how everything is defined and label from the beginning.

  1. Models will predict accidents which ended up with people severely injured or dead. This is represented by 1 or positive case.
  2. As a consequence, accidents without severely injured or dead people are represented by zero and considered negative.


In this case, we are working with a very imbalanced dataset: more than 97.5% accidents have no people injured or the injuries are minor. This excludes using accuracy as the metric and complicates the process in a deeper extent.
My goal is to predict all class 1 correctly and in doing so predict as less as possible class 0 as class 1.

Based on this:

  1. The most obvious metric to use is Recall and precision. I want to maximize recall and precision.
  2. The problem is what happens when you try to get  a high TPR: the model tends to come back with a dummy solution: predict all positive which, obviously, defeats the purpose of the project.
  3. I start using AUC_ROC to try to obtain a value over 0.7.In this phase I will also computer average precision and precision-recall as a metric.
  Other metrics that I consider are f1_score and f-beta score. Once I get a decent score for AUC, I will enter to fight this other battle.

  I will start using only the accidents file and I will move form there.

  FEATURES

  The features I will be using from the beginning are about location (neighborhood, street, longitude and latitude), time (day of the week, month, time) and finally the number of vehicles involved and the pedestrian influence in the accident.




  MODELS.

  Step 1. I started trying the classic models: LogReg, GBC and Random Forest. Logistic Regression happens to be the best one obtaining an AUC of barely 0.6.
  Step 2. I tried an approach via TensorFlow but I am not getting anything better than randomness.
  Step 3. I will try Neural Networks.
