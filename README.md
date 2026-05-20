# BarcelonaAccidents2024

---

I am trying to put together everything done by me during the last years with the dataset about the accidents in Barcelona. As a reminder, these are the accidents that took place in Barcelona, Catalonia since 2010 registered by local police.  Every March I update the dataset with the previous year data.

OBJECTIVE. Do a thorough analysis of the subject matter. It does include develop a model in ml that will predict when an accident has severely injured people or deaths, create an app via streamlit to be able to calculate probabilities of the target occurring, design a dashboard in Tableau to help us understand the dataset from different perspectives and windows of approximation.

DATA SOURCE: From the city of Barcelona open data server. https://opendata-ajuntament.barcelona.cat/en . The weather part is obtained from darksky API.

LIMITATIONS: Amongst other limitations more common in any given dataset, I only have the accidents in Barcelona during 2010-2023 reported by the Local Police (aka Guardia Urbana). Accidents not managed by Guardia Urbana are not accounted for.

DATASETS:

The final dataset used in this project is the final aggregation of the following datasets:

1. Accidents. It contains the basic information of the accident like its location (street, district, neighborhood, longitude and latitude, etc) and its timeline (month, year, day, hour) and also the cause of the pedestrian, number of deaths, injured (severe and minor) and the total of people injured and the number of vehicles involved.
2. Causes. It adds the cause of the accident when it has any cause specified. In some cases, there is more than one cause (it happens quite often) I ended up selecting the least common one.
3.People. This one adds very relevant information like the age of the people involved, the role (driver, passenger, pedestrian), the gender and the vehicle they were in.
4. Types. It indicates the general description of the accident like collision, overturning, fall, crash, etc)
5. Vehicles. This one a part from adding the color, brand and model of the vehicle, also gives us the type of license that the driver holds and his/her seniority.
6. Weather. It has the weather conditions of the city of Barcelona by the hour/half an hour.

---

 So this project will have 4 repos in order to see differents applications/perspectives to work with the dataset.

 * **Modeling**. In this part we will try to buil a model to predict if an accident manged by local police in Barcelona has any death and/or severely injured participant.
 * **Plotting**. In this section, there is going to be a collection of charts to better understand the dataset and therefore the accidents that happened in gthe city since 2010.
 * **Tableau**. Building some cool dashboards and else to showcase and investigate the accidents from different perspectives.
 * **Streamlit**. I will create an app to calculate what is the probability that any given accident will have deads and/or severely injured people.

    
