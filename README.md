# BarcelonaAccidents
Let's find out what we can learn about the accidents and therefore prevent them. In order to do this we will be analyzing this database.
This data set is obtained in open data Barcelona webpage and available to everybody ready to dig in. This is my modest homage to all of you, fellow Catalans!!!!!
Here we have some description:

1. Dataset contains all the accidents that the local police attended from 2010 to 2020. It does not include any accident that was not reported to the local police of Barcelona (aka Guardia Urbana).
2. The information gathered comes from different CSV files:

    - Accidents. This one has all information about the accident including time, location, number of victims, deceased and vehicles. It also includes a column in which it is named pedestrian cause where with many unknown values.
    - Causes of the accident. This one adds 'initial_street' and 'mediate_cause'. While the meaning of the first added column is unclear and will need further analysis, the second one -'mediate_cause' - indicates the reason - if any - behind the accident (drunk driving, damaged road, etc).
    - People. Incorporates information about the people involved in the accidents like age, gender, degree of injuries, who is responsible etc
    - Types. This CSV adds a filed named 'accidents_details' and it describes the type of accident lateral collision, run  over, etc.
    - Vehicles involved. This file adds a bunch of details about the vehicle involved from a description of it up to its model and brand name. It also includes info about the experience of the driver (type of license and experience driving).
3. It has been a hard work to combine all different CSV due to different encodings and column's names. Once I have done it, I am working with the first file to analyze the data:Barcelona_accidents. From there I will start adding more information contained in the rest of the files and will give it a try with weather data too.

TARGET. I decided to try to predict if an accident has any severely injured or deaths. This is how I created a new column that I called "target". Its value is one if the accident has any deaths and/or severely injured people, 0 if there are no injuries or these are minor. The idea is to be able to create a model that anticipates what accidents might need to be  prioritized.
I want to point out that I did also consider to include the minor injuries in the target but I finally rejected the idea.

METRICS. Once defined the target it is time to decide what the best metric is. First of all, it is a binary classification problem. Secondly, and just to be clear, I want to explain how everything is defined and label from the beginning.

  1. Models will predict accidents which ended up with people severely injured or dead. This is represented by 1 or positive case.
  2. As a consequence, accidents without severely injured or dead people are represented by zero and considered negative.


In this case, we are working with a very imbalanced dataset: more than 97.5% accidents have no people injured or the injuries are minor. This excludes using accuracy as the metric and complicates the process in a deeper extent.
My goal is to predict all class 1 correctly and in doing so predict as less as possible class 0 as class 1.

Based on this:

  1. The most obvious metric to use is recall and/or precision in an imbalanced dataset. I want to focus more in recall to prevent false negatives.
  2. I start using AUC_ROC to evaluate the model and be able to play with the threshold, if necessary. I added accuracy because I want to make sure that it does not go below 70%. A model that is over 30% wrong might lose interest.
