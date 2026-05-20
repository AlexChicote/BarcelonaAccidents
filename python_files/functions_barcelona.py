import math
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import json
import pandas as pd
import random
import numpy as np
import os
import time


from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import KNNImputer

from .paths_mapping import *


def read_df(base_dir,pathname):
    print(f'Working with...{pathname}')
    encodings = ['utf-8', 'latin-1']
    for enc in encodings:
        try:
            df = pd.read_csv(base_dir+pathname, encoding = enc, engine='python')
            print(f"{pathname} successfully read with {enc}")
            return df
            break
        except:
            try:
                df = pd.read_csv(base_dir+pathname, encoding = enc, sep=';')
                print(f"{pathname} successfully read with {enc}")
                return df
                break
            except UnicodeDecodeError:
                continue
    else:
        raise Exception(f"unable to decode the file {pathname}")


def fixing_columns(dataframe):
    """
        Changes column names to have the same column names
    """
    dataframe.columns =[col.replace("ú",'u').replace("ó","o").replace("'",'').replace(' ','_').replace("_de_","_").replace("í","i").replace("¢",'o') for col in dataframe]
    dataframe = dataframe.rename(columns=mapping_original_columns,)
   
    return dataframe



def fixing_lat(row):
    if row['lat'] == -1:
        return row['lon_lat_check'] + 1000
    if pd.isnull(row['lat']) is None:
        return row['lon_lat_check'] + 10000
    if 41.5>row['lat'] >41.2000:
        return row['lon_lat_check']
    else:
        return row['lon_lat_check'] + 1
        
def fixing_lon(row):
    if row['lon'] == -1:
        return row['lon_lat_check'] + 1000
    if pd.isnull(row['lon']) is None:
        return row['lon_lat_check'] + 10000
    if 2.27>row['lon'] >2.06:
        return row['lon_lat_check']
    else:
        return row['lon_lat_check'] + 1

def concatenating_dataframes(filter_,response):
    """Not used so far"""
    files=response['result']['results']
    for num, file in enumerate(files):
        
        if (('accidents-' +filter_+'gu') in file['name']) or ('accidents_' +filter_+'gu') in file['name']:
            #print(file['name'])
            filter_list=[]
            
            for fitxer in file['resources']:

                if fitxer['format']=='CSV':
                    
                    try:
                        filter_list.append(pd.read_csv(fitxer['url']))
                        #print(pd.read_csv(fitxer['url']).shape)
                    except:
                        try:
                            filter_list.append(pd.read_csv(fitxer['url'],encoding='ISO-8859-15'))
                            #print(pd.read_csv(fitxer['url']).shape)
                        except:
                            try:
                                filter_list.append(pd.read_csv(fitxer['url'],encoding="ISO-8859-1"))
                                #print(pd.read_csv(fitxer['url']).shape)
                            except :
                                filter_list.append(pd.read_csv(fitxer['url'],sep=';',encoding='ISO-8859-1'))
                    

    try:
        return filter_list
    except:
        print('NO FILE WITH THAT FILTER')
   





def utmToLatLng(zone, easting, northing, northernHemisphere=True):
    """Not used so far"""
   
    
    if not northernHemisphere:
        northing = 10000000 - northing

    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996
    
    
    arc = northing / k0
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

    ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

    ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

    cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    cc = 151 * math.pow(ei, 3) / 96
    cd = 1097 * math.pow(ei, 4) / 512
    phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

    n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

    r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
    fact1 = n0 * math.tan(phi1) / r0

    _a1 = 500000 - easting
    dd0 = _a1 / (n0 * k0)
    fact2 = dd0 * dd0 / 2

    t0 = math.pow(math.tan(phi1), 2)
    Q0 = e1sq * math.pow(math.cos(phi1), 2)
    fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

    fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

    lof1 = _a1 / (n0 * k0)
    lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
    lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
    _a3 = _a2 * 180 / math.pi

    latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

    if not northernHemisphere:
        latitude = -latitude

    longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

    return latitude, longitude
##correcting graphics of the letters. Having different accents and definitions is better if we get all names the same

def posant_accents(it):

    if type(it) == str:

        ##lletra ç

        if '\x87' in it:
            nova = it.replace('\x87','ç')
        elif 'Ă§' in it:
            nova = it.replace('Ă§','ç')
        
        else:
            nova = it

        ###lletra i
        if '¡' or 'Ã¯'or 'ï'or 'Ã\xad'or 'í' or '83Â\xad' or 'ÃÂ' in nova:
            renova = nova.replace('¡', 'i').replace('Ã¯', 'i').replace('ï', 'i').\
            replace('Ã\xad', 'i').replace('í', 'i').replace('83Â\xad','i').replace('ÃÂ','i')
        else:
            renova = nova
        ###Lletra o
        if '\x95' or 'Ã³' or '¢' or 'ã³'or 'Ã²' or 'ò' or 'x83Â³' or '83Â²' or 'ÃÂ³' in renova:
            trinova = renova.replace('\x95', 'o').replace('Ã³', 'o')\
            .replace('¢', 'o').replace('ã³', 'o').replace('Ã²', 'o').replace('ò', 'o').replace('x83Â³','o').replace('83Â²','o').replace('ÃÂ³','o')
        else:
            trinova = renova

        if '¢' in trinova:

            quatrinova = trinova.replace('¢', 'o')
        else:
            quatrinova = trinova

        ###lletra e
        if '\x82' or 'Ã©' or 'é' or 'è'or 'Ãš' or '\x8a' or 'č' or 'x83Â©' in quatrinova:
            cinquinova = quatrinova.replace('\x82', 'e').replace('Ã©', 'e').replace('é', 'e').replace('è', 'e').\
            replace('Ãš', 'e').replace('\x8a', 'e').replace('č','e').replace('x83Â©','e')
        else:
            cinquinova = quatrinova
          
        ###lletra a
        if '\x85' or 'Ã\xa0' or '' or '83Â\xa0' or 'ÃÂ' or 'ÃÂ ' in cinquinova:
            sixinova = cinquinova.replace('\x85', 'a').replace('Ã\xa0', 'a').replace('à', 'a').replace('83Â\xa0','a').replace('ÃÂ','a').replace('ÃÂ ','a')
        else:
            sixinova = cinquinova

        if 'Sarr' in sixinova:

            septinova = 'Sarria'
        else:
            septinova = sixinova

        if 'Ã§' in septinova:
            vuitinova = septinova.replace('Ã§', 'ç')
        else:
            vuitinova = septinova

        ##Lletra u
        if 'ãº' or 'ú' or '£'in vuitinova:
            nounova = vuitinova.replace('ãº', 'u').replace('ú', 'u').replace('£','u')
        else:
            nounova = vuitinova

        if 'ã³' or 'ó' in nounova:

            deunova = nounova.replace('ã³', 'o').replace('ó', 'o')
        else:
            deunova = nounova
       
    else:
        deunova = it

    return deunova

####Causes a angles

def cause_to_angles(it):
    
    """Up until 2023 the data used 'No hi ha causa mediata' 
        when no cause is assign to accident. In 2024 they use blanks
    """

    cause_dict={'Alcoholemia': 'DrunkDriving',
               'Calçada en mal estat': 'Damaged_road',
               'Drogues o medicaments': 'DUI',
               'Estat de la senyalitzacio': 'Damaged_signal',
               'Exces de velocitat o inadequada': 'Speeding',
               'Factors meteorologics': 'Weather',
                'Objectes o animals a la calçada': 'Objects or animals on the road',
                'No hi ha causa mediata': 'No mediate cause'}


    return cause_dict.get(it,"No mediate cause")

##transalting to Catalan

def traduir_castella(word):
    if type(word) == str:
        if word.endswith('ismo'):
            nova = word.replace('ismo', 'isme')
        else:
            nova = word
        if 'ciclo' in nova:
            renova = nova.replace('ciclo', 'cicle')
        else:
            renova = nova

        if renova.startswith('Cuadri'):
            trinova = renova.replace('Cuadri', 'Quadri')
        else:
            trinova = renova

        if trinova.startswith('Camion'):

            quatrinova = trinova.replace('Camion', 'Camio rigid')

        else:
            quatrinova = trinova

        if quatrinova.endswith('  camion'):

            cinquinova = quatrinova.replace('camion', 'camio')
        else:
            cinquinova = quatrinova

        if 'Tm'in cinquinova:
            sixinova = cinquinova.replace('Tm', 'tones')
        else:
            sixinova = cinquinova
        if '75cc' in sixinova:
            septinova = sixinova.replace('75cc', ' 75 cc')
        else:
            septinova = sixinova
        if '> 75' in septinova:
            octinova = septinova.replace('> 75', '>= 75')
        else:
            octinova = septinova
        if octinova == 'Tranvia o tren':
            noninova = 'Tren o tramvia'
        else:
            noninova = octinova
        if 'de obras' in noninova:
            nova2 = noninova.replace('de obras', "d'obres i serveis")
        else:
            nova2 = noninova

        if 'Otros' or 'terreno' or 'articulado' or 'vehic. a' or 'Todo' or '17 plazas' in nova2:

            nova3 = nova2.replace('Otros', 'Altres').replace('terreno', 'terreny').\
            replace('articulado', 'articulat').replace('vehic. a', 'vehicles amb').replace('Todo', 'Tot')\
            .replace('17 plazas',' 17')
        else:
            nova3 = nova2
        if nova3 == 'Tractocamion':
            nova4 = "Tractor camio"
        else:
            nova4 = nova3
    else:
        nova4 = word

    return nova4

def ped_to_angles(row):

    """Up until 2023 the data used 'Desconegut' or 'No es causa...'
        when no ped caused the acc. In 2024 they use blanks as they did in early years
    """

    ped_dict={'Desconegut': 'No peds fault',
             'Creuar per fora pas de vianants': 'Crossing outside ped crossing',
             'Desobeir el senyal del semàfor': 'Disobey the traffic light',
             'Transitar a peu per la calçada': 'Walk on the road',
             'Altres': 'Other',
             'Desobeir altres senyals': 'Disobey other signals',
             'No es causa del  vianant': 'No peds fault',
             'No és causa del  vianant': 'No peds fault'}

    return ped_dict.get(row['ped_cause'],'No peds fault') 


def setmana_a_angles(row):

    dia_dict={'Dilluns': 'Monday',
             'Dimarts': 'Tuesday',
             'Dimecres': 'Wednesday',
             'Dijous': 'Thursday',
             'Divendres': 'Friday',
             'Dissabte': 'Saturday',
             'Diumenge': 'Sunday',}
    return dia_dict.get(row['weekday'],'NotFound')


def mes_a_angles(row):

    mes_dict={'Gener': 'January',
             'Febrer': 'February',
             'Març': 'March',
             'Abril': 'April',
             'Maig': 'May',
             'Juny': 'June',
             'Juliol': 'July',
             'Agost': 'August',
             'Setembre': 'September',
             'Octubre': 'October',
              'Novembre':'November',
              'Desembre':'December'
             }

    return mes_dict.get(row['month'],'NotFound')

def mes_english_number(mes):

    mes_dict={'January': '01',
             'February': '02',
             'March': '03',
             'April': '04',
             'May': '05',
             'June': '06',
             'July': '07',
             'August': '08',
             'September': '09',
             'October': '10',
              'November':'11',
              'December':'12'}

    return mes_dict[mes]

def counting_non_zeros(tup):
    count = 0
    for i in tup:
        if i > 0:
            count+=1
    if count == 0:
        count = 1
    return count

def debugging_strings(row, word):
    word = str(word)
    count = 0
    for i in row:
        if word in i:
            count =1
    return count

def mercedes(word):
    """Corregir tots els mercedes"""
    if word in ['mercedes-benz', 'mercedesb', 'mecedes']:
        word = 'mercedes'
    return word


def licenses(license):

    license_dict={'A': 'motorbike_license',
             'BTP': 'taxis_ambulances_license',
             'B': 'regular_license',
             'D': 'bus_license',
             'C': 'van_license'}

    return license_dict[license]

def fixing_codes(i):

    if i in desconegut_llista:
        i = int(-1)
    elif type(i) == float:
        i = int(i)

    elif (type(i) == str) and len(i) > 4:
        i = int(''.join(i.split("-", 2)[2:]))
    elif (type(i) == str) and len(i) <= 4:
        i = int(''.join(i.split('.')[0]))

    else:
        i = int(i)
    return i


def scraping_weather(date):
    url=f'https://www.meteo.cat/observacions/xema/dades?codi=D5&dia={date}T13:00Z'
    df = pd.read_html(url)[-1]
    df.rename(columns=renaming_columns,inplace=True)
    df['date']=date
    return df


def fixing_datetime_format(row):
    '''Form some reason, datetime for some year is in utc format while the rest are not'''
    return row['datetime'][:19]


def creating_datetime(row):
    full_datetime=row['date']+' '+row['period_UT'][:5]
    return full_datetime


def creating_yearly_weather(year,pathname=WEATHER_PATH):
    if f'weatherbarcelona{year}.csv' in os.listdir(pathname):
        weather_year=pd.read_csv(pathname+f'weatherbarcelona{year}.csv')
        print(f"Done with {year}")
        
    else:
        weather_year=pd.DataFrame()
        dates=pd.date_range(start=str(year)+'-01-01', end=str(year)+'-12-31')
        count=0
        for date in dates:
            #print(date)
            df=scraping_weather(str(date)[:10])
            df['datetime']=pd.to_datetime(df.apply(creating_datetime,axis=1))
            df.drop(['date','period_UT'],axis=1,inplace=True)
            count+=1
    
            if count%90==0:
                print(date)
                time.sleep(3)
            
            if weather_year.empty:
                weather_year=df
            else:
                weather_year=pd.concat([weather_year,df])
    
        weather_year.reset_index().to_csv(WEATHER_PATH / f'weatherbarcelona{year}.csv',index=False)
        print(f"Done with {year}")
    
    if 'weatherfinal.csv' in os.listdir(pathname):
        weather=pd.read_csv(pathname+'weatherfinal.csv',low_memory=False)
        weather['datetime']=pd.to_datetime(weather.datetime,utc=True,format='mixed',yearfirst=True)
        if year not in list(weather.datetime.dt.year):
            weather=pd.concat([weather,weather_year])
            weather.to_csv(pathname+'weatherfinal.csv',index=False)
    else:
        weather_year.to_csv(pathname+'weatherfinal.csv',index=False)


def imputing_nulls(dataframe):
    # 1. Create sample dataset (Nulls in both numerical and categorical columns)
    dataframe.set_index('num_incident',inplace=True)
    
    num_cols = list(dataframe.describe().columns)
    cat_cols = [col for col in dataframe.columns if col not in num_cols]
    # 2. Use OrdinalEncoder while preserving NaN values
    # handle_unknown='use_encoded_value' keeps NaNs intact as np.nan
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', MinMaxScaler(), num_cols),
            ('cat', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=np.nan), cat_cols)
        ]
    )
    
    # Transform data to numeric format (keeps NaNs as NaN)
    X_processed = preprocessor.fit_transform(dataframe)
    
    # 3. Apply KNNImputer
    imputer = KNNImputer(n_neighbors=2)
    X_imputed = imputer.fit_transform(X_processed)
    
    # 4. Separate numerical and categorical parts
    num_features_len = len(num_cols)
    X_num_imputed = X_imputed[:, :num_features_len]
    X_cat_imputed = X_imputed[:, num_features_len:]
    
    # 5. CRITICAL: Round categorical codes to nearest integer before decoding
    # KNN output averages like 0.5 must become 1.0 or 0.0 to match original categories
    X_cat_rounded = np.round(X_cat_imputed)
    
    # 6. Inverse transform to return to original scales
    scaler = preprocessor.named_transformers_['num']
    encoder = preprocessor.named_transformers_['cat']
    
    X_num_original = scaler.inverse_transform(X_num_imputed)
    X_cat_original = encoder.inverse_transform(X_cat_rounded)
    
    # 7. Rebuild the final DataFrame
    df_num_final = pd.DataFrame(X_num_original, columns=num_cols)
    df_cat_final = pd.DataFrame(X_cat_original, columns=cat_cols)
    df_final = pd.concat([df_num_final, df_cat_final], axis=1)
    df_final.index = dataframe.index
    
    return df_final



def assigning_vehicle_to_group(row):
    """Based on a classification done, we bucketinize vehicles
    """
    for key in vehicle_grouping:
        if row['vehicle'] in vehicle_grouping[key]:
            return key

def assigning_type_to_group(row):
    """Based on a classification done, we bucketinize accident types
    """
    for key in type_grouping:
        if row['accident_type'] in type_grouping[key]:
            return key

            
def organizing_types(string,type_list):
    set_string=set(string.split(','))
    if len(set_string)==1:
        return str(set_string)[2:-2]
    else:
        for ty in type_list:
            if ty in set_string:
                set_string.remove(ty)
                if len(set_string)==1:
                      return str(set_string)[2:-2]
        
    return set_string


def remove_accents(word):
    
    return word.replace('à', 'a').replace('è','e').replace('é', 'e').replace('ï', 'i').replace('í', 'i').replace('ò','o').replace('ó', 'o').replace('ü','u').replace('ú', 'u')


def common_member(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set): 
        print(a_set & b_set) 
    else: 
        print("No common elements")
        
def common_member_and_number(a,b):
    a_set = set(a) 
    b_set = set(b) 
    llista = []
    if (a_set & b_set): 
        llista = list(a_set & b_set) 
    return llista
def set_of_colors(n):
    color = []
    for i in range(n):
        color.append('#%06X' % random.randint(0, 0xFFFFFF))    
    return color

def random_color_generator(n):
    colors=[]
    for i in range(n):
        color = np.random.randint(0, 256, size=3)
        colors.append(tuple(color))
    return colors

def fixing_seniority(string):
    """Will replace Desconegut with null"""
    string=string.split(',')
    return string