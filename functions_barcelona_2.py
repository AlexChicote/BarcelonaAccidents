
import pandas as pd
import functions_barcelona as fb
import datetime
try:
    from holidays_es import Province
    festes=True
except:
    festes=False
    
import numpy as np
import os

from sklearn.metrics import recall_score, precision_score, accuracy_score, roc_auc_score
from sklearn.model_selection import KFold, cross_val_score, cross_validate, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MinMaxScaler, StandardScaler,Normalizer
from xgboost import XGBClassifier

# from imblearn.over_sampling import SMOTE, ADASYN, RandomOverSampler
# from imblearn.under_sampling import RandomUnderSampler, NearMiss
from sklearn.dummy import DummyClassifier
import imblearn.under_sampling as under
import imblearn.over_sampling as over
import imblearn.combine as over_under
from imblearn.pipeline import Pipeline, make_pipeline

###importing dataset

accidents=pd.read_csv('../data/weather_accidents_2010_20.csv')


for col in accidents:
    if 'Unnamed' in col:
        accidents=accidents.drop(col,axis=1)
# accidents['month']=accidents['month'].apply(fb.mes_english_number)
# date_columns = ['month', 'day', 'year','hour']
# date = accidents[date_columns]
# dates = []
# datetimes=[]
# for i in date.itertuples():
#     dates.append(i[1]+'/' +str(int(i[2]))+'/'+str(int(i[3])))
#     datetimes.append(i[1]+'/' +str(int(i[2]))+'/'+str(int(i[3]))+' '+str(int(i[4]))+':00:00')

# accidents['dates']=dates
# accidents['datetimes']=datetimes
accidents['dates']=pd.to_datetime(accidents.dates)
accidents['datetimes']=pd.to_datetime(accidents.datetimes)

accidents['target']=accidents['num_deaths']+accidents['num_severly_injured']
accidents['target']=[1 if compte>0 else 0 for compte in accidents.target]
##eliminant features leaking and/or irrelevant
# accidents=accidents.drop(['index','num_incident', 'num_deaths', 'num_minorly_injured', 'num_severly_injured',
#        'num_victims',],axis=1)



##Creating new features
##FEATURE ENGINEERING
#1. Classifying streets by level of accidents
num=10
labels=range(num)
accidents['street_count']=pd.qcut(accidents.street_code.map(accidents.street_code.value_counts().to_dict()),
                                  num,
                                  labels=labels)
#2. Identifying accidents that ocurr in a crossing
accidents['crossing_street']=[1 if '/' in x else 0 for x in accidents.street_name]
#3. Are pedestrians involved?
#accidents['pedestrian']=[0 if x=='unknown' else -1 if x=='No peds fault' else 1 for x in accidents.ped_cause]
accidents['pedestrian']=[1 if x=='unknown' else 0 for x in accidents.ped_cause]
#4. Creating shifts feature
accidents['hour']=accidents['hour'].astype(int)
accidents['shift']=['Night' if x >21 or x<6 else 'Morning' if x < 14 else 'Afternoon' for x in accidents.hour]
#5. Creating weekend feature. Seems to be a pick in the ratio deaths per accident
accidents['weekend']=[1 if day in ['Friday','Saturday','Sunday'] else 0 for day in accidents.weekday]
##Including Monday in the weekend
accidents['long_weekend']=[1 if day in ['Friday','Saturday','Sunday','Monday'] else 0 for day in accidents.weekday]
##making different levels for weekdays. Saturday more risky and Tuesday not all all
accidents['weekday_risklevel']=[1 if x=='Saturday' else -1 if x=='Tuesday' else 0 for x in accidents.weekday]
#6. Binning neighborhoods
num=6

labels=range(1, num)
accidents['hood_count']=pd.qcut(accidents.neighborhood.map(accidents.neighborhood.value_counts().to_dict()),
                                  num,
                                  labels=False,
                               #duplicates='drop',
                                #retbins=True
                               )

#7. CREATING HOLIDAY COLUMN. Assign 1 if holiday, -1 if previoous to holiday and 0 if non

if festes:

    total_holidays=[]
    for year in range(2010,2021):
        holidays = Province(name="barcelona", year=year).holidays()
        for key in holidays.keys():
            total_holidays.extend(holidays[key])
    ##Hoiliday is 1 holiday eve is -1 the rest are 0        
    accidents['holidays']=[1 if date.date() in total_holidays else -1 if -1 in [(date.date()-date_h).days for date_h in total_holidays] else 0 for date in accidents.dates]

    num_holidays=len(total_holidays)

    working_days=['Monday', 'Tuesday','Wednesday','Thursday','Friday']
    accidents['real_holidays']=[1 if x[0] ==1 or x[1] in ['Saturday', 'Sunday'] else 0 for x in zip(accidents['holidays'], accidents['weekday'])]
    accidents['holiday_eve']=[1 if (x[0]==-1) or (x[1] in ['Friday', 'Saturday']) else 0 for x in zip(accidents['holidays'], accidents['weekday'])]
    accidents['weekend']=[1 if x in ['Saturday', 'Sunday'] else 0 for x in accidents.weekday]
    accidents['workingday']=[1 if (x[1] in working_days) and (x[0]==0) else 0 for x in zip(accidents['holidays'], accidents['weekday'])]

calendar=pd. date_range(start=datetime.date(2010,1,1),end = datetime.date(2020,12,31)). to_pydatetime(). tolist()
calendar=[x.date() for x in calendar]
accidents_dates=list(set([x.date() for x in accidents.dates]))
#print("DAYS WITH NO ACCIDENTS\n")
days_with_no_accidents=[x for x in calendar if x not in accidents_dates] 

#8. Binning weather desPoint

num=5
labels=range(num)
accidents['weather_binning_dewPoint']=pd.qcut(accidents.weather_dewPoint,
                                  num,
                                  labels=False)
point_1=accidents.weather_dewPoint.max()
point_5=accidents.weather_dewPoint.min()
margin=(point_1-point_5)/4
point_2=point_1-margin
point_3=point_2-margin
point_4=point_3-margin
#[point_1,point_2, point_3,point_4,point_5]

def binning_dewPoint(value):
    if value>point_2:
        return 'group 1'
    elif value>point_3:
        return 'group 2'
    elif value> point_4:
        return 'group 3'
    else: return 'group 4'
    
accidents['weather_binning_dewPoint2']=accidents['weather_dewPoint'].apply(binning_dewPoint)
##collapsing categories in summary
accidents['weather_summary']=['Windy'  if 'Windy' in x else \
           'Humid' if 'Humid' in x else\
           'Rain' if 'Sleet' in x or 'Flurries' in x else x for x in accidents.weather_summary]

accidents['people_role_pass']=[float(x) if float(x)<6 else 10 for x in accidents.people_role_pass]
accidents.to_csv('/Users/fcbnyc/mystuff/repos/BarcelonaAccidents/FINAL_FILES/data/clean_accidents.csv')

##Preparing data train and test

test=accidents[accidents.year.isin([2019,2020])].reset_index()
train=accidents[~accidents.year.isin([2019,2020])].reset_index()
X_train=train.drop('target',axis=1)
y_train=train.target
X_test=test.drop('target',axis=1)
y_test=test.target


###Organizing features from accidents
random_state=55
feature_dict={}
no_features=['num_victims','num_incident','target','num_deaths',\
                          'num_minorly_injured', 'num_severly_injured','index']
feature_dict['features']=[col for col in accidents.columns if col not in no_features]

pending_features=feature_dict['features'].copy()

feature_dict['binary_features']=[x for x in pending_features if accidents[x].nunique()==2]
pending_features=[x for x in pending_features if x not in feature_dict['binary_features']]

feature_dict['numerical_features']=[x for x in pending_features if accidents[x].dtypes=='float64']
feature_dict['numerical_features'].append('num_vehicles')
pending_features=[x for x in pending_features if x not in feature_dict['numerical_features']]

feature_dict['datetime_features']=[x for x in pending_features if 'date' in x]
pending_features=[x for x in pending_features if x not in feature_dict['datetime_features']]
##The rest are all categorical
feature_dict['categorical_features']=pending_features.copy()
feature_dict['binned_categorical_features']=['street_count','weekday_risklevel','hood_count','holidays','weather_binning_dewPoint','weather_binning_dewPoint2']
pending_features=[x for x in pending_features if x not in feature_dict['binned_categorical_features']]
feature_dict['ordinal_categorical_features']=['weekday','year','month','day','hour','shift']
feature_dict['cardinal_categorical_features']=[x for x in pending_features if x not in feature_dict['ordinal_categorical_features']]
target=['target']
###Metrics and models


models=['dummyclassifier','logreg', 'random_forest','GradienBoostClassifier']
metrics=['recall','precision','accuracy','roc_auc']
models_dict = {
    'dummy': {'name': DummyClassifier(strategy='stratified')},
    'logreg': {'name': LogisticRegression(C= 1e9, random_state=random_state,class_weight='balanced')},
'forest':{'name': RandomForestClassifier(class_weight='balanced', max_depth=5, n_estimators=10, max_features=3, random_state=random_state)}, 
'gbc': {'name': GradientBoostingClassifier(random_state=random_state, learning_rate=0.01,min_samples_split = 500,\
                                          min_samples_leaf = 50, max_depth = 8,max_features = "sqrt",\
                                          subsample = 0.8)},}

##list of models to use to compare results in cross validation

models_list=[]
models_list.append(('logreg',LogisticRegression(C= 1e9, random_state=random_state,class_weight='balanced',max_iter=1000)))
models_list.append(('rf',RandomForestClassifier(class_weight='balanced', max_depth=3, n_estimators=10, max_features=3, random_state=random_state)))
models_list.append(('lda', LinearDiscriminantAnalysis()))
models_list.append(('linearsvc',LinearSVC(C=1.0, random_state=random_state, class_weight='balanced')))
models_list.append(('knn', KNeighborsClassifier()))
models_list.append(('GNB',GaussianNB()))
models_list.append(('XGB',XGBClassifier(scale_pos_weight=97,random_state=random_state,eval_metric='auc')))
##Building X_train and y_train, X_test and y_test with features

def preprocessing_fetures(train,test,numerical_features, categorical_features,scaler=True):
    
   
    
    X_train=pd.concat(
        [train[numerical_features],pd.get_dummies(train[categorical_features],drop_first=True)],
        axis=1)
    
    X_test=pd.concat(
        [test[numerical_features],pd.get_dummies(test[categorical_features],drop_first=True)],
        axis=1)
    
    if scaler:
        scaler=Normalizer()
        X_train=scaler.fit_transform(X_train)
        X_test=scaler.transform(X_test)
    
    return X_train,X_test


###Undersampling

def undersampling_dataset(X,y,model=under.RandomUnderSampler(random_state=random_state)):
    model_under=model
    X_under, y_under = model_under.fit_resample(X, y)
    
    return X_under,y_under

def oversampling_dataset(X,y,model=over.RandomOverSampler(random_state=random_state)):
    model_over=model
    X_over, y_over = model_over.fit_resample(X, y)
    
    return X_over,y_over


def scoring_model(X_train,X_test,y_train,y_test,model):
    model.fit(X_train,y_train)
    predictions=model.predict(X_test)
    metrics_dict={'recall':recall_score(y_test,predictions),
                 'precision': precision_score(y_test,predictions),
                 'accuracy': accuracy_score(y_test,predictions),
                 'auc': roc_auc_score(y_test,predictions)}
    scores=[]
    for key in metrics_dict.keys():
        scores.append(metrics_dict[key])
    return scores


def scoring_model_cv(X_train,y_train,models_list):
    """List has to be a tuple being the first part the name of the model and the second the class to run it"""
    dic={}
    kfold=KFold(n_splits=5, random_state=random_state, shuffle=True)
    for model in models_list:
        dic[model[0]]={}

        for metric in [y for y in metrics if y!='auc']:
            cv_results=cross_val_score(model[1], X_train,y_train, cv=kfold, scoring=metric)
            dic[model[0]][metric]=cv_results
       
    return dic
    
                   


undersamplings={'allKNN': under.AllKNN(),
              'CC': under.ClusterCentroids(random_state=random_state),
              'ENN': under.EditedNearestNeighbours(n_neighbors=3, kind_sel='mode'),
              'REN': under.RepeatedEditedNearestNeighbours(),
              'IHT': under.InstanceHardnessThreshold(random_state=random_state),
              'NM1': under.NearMiss(version=1),
              'NM3': under.NearMiss(version=3),
              'NCL': under.NeighbourhoodCleaningRule(),
              'OSS': under.OneSidedSelection(random_state=random_state),
              'RUS': under.RandomUnderSampler(random_state=random_state),
              'TL': under.TomekLinks()}

oversamplings={'ADASYN': over.ADASYN(random_state=random_state),
              'BSMOTE': over.BorderlineSMOTE(random_state=random_state),
              #'KMeansSMOTE': over.KMeansSMOTE(random_state=random_state),
              'SMOTE': over.SMOTE(random_state=random_state),
              'SMOTEN': over.SMOTEN(random_state=random_state),
            #'SMOTENC':over.SMOTENC(categorical_features=categorical_features,random_state=random_state),
              'SVMSMOTE': over.SVMSMOTE(random_state=random_state),
              'ROS': over.RandomOverSampler(random_state=random_state),
              }

over_undersamplings={'SMOTEENN': over_under.SMOTEENN(random_state=random_state),
              'SMOTETomek': over_under.SMOTETomek(random_state=random_state),
              }

