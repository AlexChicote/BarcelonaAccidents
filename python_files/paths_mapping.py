from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
#print(BASE_DIR)
WEATHER_PATH = BASE_DIR/'modeling'/ 'data'/'weather'
#print(WEATHER_PATH)
FILES_PATH = BASE_DIR /'modeling'/ 'data'
# print(FILES_PATH)
SHAPEFILES_PATH = BASE_DIR/'Tableau'/'shapefiles'
print(SHAPEFILES_PATH)

##mappings

renaming_columns={'PeríodeTU':'period_UT',
                  'TM°C':'temp_avg',
                  'TX°C':'temp_max',
                  'TN°C':'temp_min',
                  'HRM%': 'relative_humidity',
                  'PPTmm':'precipitation',
                  'VVM (10 m)km/h': 'windspeed',
                   'DVM (10 m)graus': 'wind_direction',
                  'VVX (10 m)km/h' : 'max_windspeed',
                  'PMhPa': 'pressure',
                  'RSW/m2':'solar_radiation'}


mapping_gender ={'Home': 0,
                 'H': 0,
                'Dona': 1,
                 'D': 1,
                'Desconegut':-1,}

mapping_role ={'Conductor': 'driver',
                'Passatger':'passenger',
                'Vianant':'pedestrian',
              'Desconegut':'unknown',}

mapping_vehicles={'Motocicleta': 'motorcycle',
                  'Tricicle':'tricycle',
                  'Bicicleta pedaleig assistit': 'personal non-motor vehicles',
                    'Ambulància':'ambulance',
                    'Ciclomotor': 'moped',
                    'Turismo': 'car',
                    'Furgoneta':'van',
                    'Bicicleta':'bicycle',
                    'Taxi':'taxi',
                    'Tranvía o tren':'tram',
                    'Autobús':'bus',
                    'Cuadriciclo >=75cc':'quadricycle over 75cc',
                    'Camión <= 3,5 Tm':'truck under 3.5 tons',
                    'Microbus <=17 plazas': 'minibus <17 pass',
                    'Camión > 3,5 Tm':'truck over 3.5 tons',
                    'Autobús articulado':'articulated bus',
                    'Tractocamión':'tractor-truck',
                    'Todo terreno':'suv',
                    'Cuadriciclo <75cc':'quadricycle under 75cc',
                    'Otros vehíc. a motor':'other motor vehicles',
                    'Autocar':'bus',
                    'Maquinaria de obras':'construction machinery',
                    'Autob£s':'bus',
                    'Otros veh¡c. a motor':'other motor vehicles',
                    'Cami¢n <= 3,5 Tm':'truck under 3.5 tons',
                    'Autob£s articulado':'articulated bus',
                    'Cami¢n > 3,5 Tm':'truck over 3.5 tons',
                    'Tranv¡a o tren':'tram',
                    'Tractocami¢n':'tractor-truck',
                    'Autocaravana':'camper',
                    'Turisme':'car',
                    'Autobús articulat':'articulated bus',
                    'Altres vehicles sense motor':'other non-motor vehicles',
                    'Camió rígid <= 3,5 tones':'truck under 3.5 tons',
                    'Altres vehicles amb motor':'other engine vehicles',
                    'Quadricicle > 75 cc':'quadricycle over 75cc',
                    'Camió rígid > 3,5 tones':'truck over 3.5 tons',
                    'Tren o tramvia':'tram',
                    'Maquinària d"obres i serveis':'construction machinery',
                    'Tractor camió': 'tractor-truck',
                    'Tot terreny':'suv',
                    'Quadricicle < 75 cc':'quadricycle under 75cc',
                    'Desconegut':'unknown',
                    'Sense Informar':'unknown',
                    'Microbus <= 17': 'minibus <17 pass',
                    'Veh. mobilitat personal amb motor': 'personal motor vehicles',
                    'Veh. mobilitat personal sense motor':'personal non-motor vehicles',
                    'Microbús <= 17': 'minibus <17 pass',
                    'Carro':'wagon',
                    'Pick-up':'van',
                    "Maquinŕria d'obres i serveis":'construction machinery',
                    "Maquinària d'obres i serveis":'construction machinery',
                    'Ambulŕncia': 'ambulance'}
mapping_types={'Atropellament': 'run_over',
        'Col.lisio lateral': 'lateral_collision',
        'Col.lisió lateral' : 'lateral_collision',
        'Xoc contra element estatic': 'crash_into_stationary',
        'Xoc contra element estàtic': 'crash_into_stationary',
      'Abast': 'rear_end_collision',
       'Col.lisio frontal':'frontal_collision',
        'Col.lisió frontal': 'frontal_collision',
      'Col.lisio fronto-lateral':'frontal_lateral_collision',
      'Col.lisió fronto-lateral': 'frontal_lateral_collision',
      'Caiguda (dues rodes)':'fall__motorcycle',
      'Abast multiple':'multiple_rear_end_collision',
      'Caiguda interior vehicle':'fall_inside_vehicle',  ##public transportation
      'Altres':'other_types',
      'Bolcada (mes de dues rodes)':'overturning',
        'Bolcada (més de dues rodes)': 'overturning',
      'Desconegut':'unknown',
      'Sortida de via amb xoc o col.lisio':'run_off_with_crash_or_collision',
        'Sortida de via amb xoc o col.lisió': 'run_off_with_crash_or_collision',
      'Encalç':'rear_end_collision',
      'Sortida de via amb bolcada':'run_off_with_overturning',
      'Xoc amb animal a la calçada':'crash_into_animal_on_road',
      'Resta sortides de via':'run_off_not_included_previously'}

mapping_injuries = {'Ferit lleu':'minor',
                    'Ferit greu':'severe',
                    'Mort':'deceased',
                   'Ferit lleu: Hospitalització fins a 24h': 'minor',
                   "Ferit lleu: Amb assistència sanitària en lloc d'accident":'minor',
                   'Ferit lleu: Rebutja assistència sanitària': 'minor',
                    "Ferit lleu: Amb assistčncia sanitŕria en lloc d'accident" : 'minor',
                    'Ferit lleu: Rebutja assistčncia sanitŕria':'minor',
                    'Ferit greu: hospitalització superior a 24h':'severe',
                    'Mort (dins 24h posteriors accident)': 'deceased',
                    'Mort (després de 24h posteriors accident)':'deceased',
                    'Mort natural': 'deceased',
                    'Il.lčs':'unharmed',
                    'Il.lès':'unharmed',
                    'Desconegut':'unkown',
                    'Es desconeix': 'unkown',
                    
                    
                   }

mapping_original_columns={"Numero_expedient": "num_incident",
                          'Ã¯Â»Â¿Numero_expedient':'num_incident',
              "Numero_d_expedient": "num_incident",
              "Numero_dexpedient": "num_incident",
              'N£mero_dexpedient': "num_incident",
              'Numero_Expedient': "num_incident",
              'Codi_expedient': 'num_incident',
              'Codi_dexpedient':'num_incident',
                "Nom_districte": "district",
              'Codi_districte': 'district_code',
              'Codi districte': 'district_code',
               "Nom_barri":"neighborhood",
              "Nom_carrer":"street_name",
              "Descripcio_dia_setmana":"weekday",
              "NK_Any":"year",
              "Any":"year",
              "Nom_mes":"month",
              "Dia_mes":"day",
              "Dia_de_mes":"day",
              "Hora_dia":"hour",
              "Descripcio_causa_vianant":"ped_cause",
              "Numero_morts":"num_deaths",
              "Numero_lesionats_lleus":"num_minorly_injured",
              "Numero_lesionats_greus":"num_severly_injured",
              "Numero_victimes":"num_victims",
              "Numero_vehicles_implicats":"num_vehicles",
              "Coordenada_UTM_X_ED50":"utm_x",
              "Coordenada_UTM_Y_ED50":"utm_y",
            "Coordenada_UTM_X":"utm_x",
             "Coordenada_UTM_Y":"utm_y",
             "Coordenada UTM (Y)": "utm_y",
             "Coordenada UTM (X)": "utm_x",
             "Coordenada_UTM_(Y)":"utm_y",
             "Coordenada_UTM_(X)":"utm_x",
             "Longitud_WGS84":"lon",
              "Long":'lon',
              "Longitud":'lon',
              "Latitud": 'lat',
             "Latitud_WGS84":"lat",
             'Num_postal_':"Num_postal",
             "Num_postal_caption":"Num_postal",
             'Tipus_accident':'accident_type',
              'Descripcio_tipus_accident':'accident_type',
              'Descripcio_color':'vehicle_color',
              'Descripcio_model':'vehicle_model',
              'Descripcio_marca':'vehicle_brand_name',
              'Descripcio_carnet': 'license',
              'Antiguitat_carnet':'license_seniority',
              'causa_mediata':'cause',
              'Descripcio_causa_mediata':'cause',
            'Descripcio_sexe':'gender',
             'Edat':'age',
            'Descripcio_tipus_persona':'people_role',
                'Desc_Tipus_vehicle_implicat': 'vehicle',
                'Desc._Tipus_vehicle_implicat': 'vehicle',
                'Descripcio_victimitzacio': 'injuries_degree'
             }

mapping_colors ={'negre': 'black',
                'blanc':'white',
                'gris':'gray',
                'altres':'other',
                'vermell':'red',
                 'blau':'blue',
                 'verd':'green',
                 'beige':'grayish tan',
                 'platejat':'silver',
                 'groc': 'yellow',
                 'taronja':'orange',
                 'daurat':'gold',
                 'violeta':'violet',
                 'rosa':'pink',
                 'negre/groc':'black/yellow',
                 'granate': 'maroon',
                 'marr¢':'brown',
                 'marr¢':'brown',
                 'marrã\x83â³':'brown',
                 'marró':'brown',
                 'marrã³':'brown',
                 'unknown':'unknown'
                }


vehicle_grouping ={
'MicroMobility' : ['motorcycle', 'moped', 'bicycle', 'quadricycles',
                 'tricycle','quadricycle under 75cc','quadricycle over 75cc',
                'personal non-motor vehicles','other non-motor vehicles'],
'LightPassenger' : ['car', 'taxi', 'personal motor vehicles', 'suv', 'camper', 'wagon'],
'MassTransit' : ['bus', 'articulated bus', 'minibus', 'tram','minibus <17 pass'],
'FreightAndLogistics' : ['van', 'all trucks', 'truck under 3.5 tons','truck over 3.5 tons','tractor-truck'],
'Specialized' : ['ambulance', 'construction machinery', 'unknown', 'other motor vehicles','other engine vehicles'],
}



vehicle_grouping_criteria ="""
The "Road Impact" Grouping (Infrastructure & Space)
This is most useful for urban planning or traffic flow analysis. It groups vehicles by their physical footprint and how they interact with the road.

Two-Wheelers & Micro-mobility (100,808): Motorcycle, moped, bicycle, quadricycles, tricycle. (The dominant group).

Light Passenger Vehicles (53,923): Car, taxi, personal motor vehicles, SUV, camper, wagon.

Mass Transit (9,073): Bus, articulated bus, minibus, tram.

Freight & Logistics (7,407): Van, all trucks, tractor-trucks.

Specialized & Other (660): Ambulance, construction machinery, unknown, others.

"""

type_accident_map={'Atropellament': 'run_over',
        'Col.lisio lateral': 'lateral_collision',
        'Col.lisió lateral' : 'lateral_collision',
        'Xoc contra element estatic': 'crash_into_stationary',
        'Xoc contra element estàtic': 'crash_into_stationary',
      'Abast': 'rear_end_collision',
       'Col.lisio frontal':'frontal_collision',
        'Col.lisió frontal': 'frontal_collision',
      'Col.lisio fronto-lateral':'frontal_lateral_collision',
      'Col.lisió fronto-lateral': 'frontal_lateral_collision',
      'Caiguda (dues rodes)':'fall__motorcycle',
      'Abast multiple':'multiple_rear_end_collision',
      'Caiguda interior vehicle':'fall_inside_vehicle',  ##public transportation
      'Altres':'other_types',
      'Bolcada (mes de dues rodes)':'overturning',
        'Bolcada (més de dues rodes)': 'overturning',
      'Desconegut':'unknown',
      'Sortida de via amb xoc o col.lisio':'run_off_with_crash_or_collision',
        'Sortida de via amb xoc o col.lisió': 'run_off_with_crash_or_collision',
      'Encalç':'rear_end_collision',
      'Sortida de via amb bolcada':'run_off_with_overturning',
      'Xoc amb animal a la calçada':'crash_into_animal_on_road',
      'Resta sortides de via':'run_off_not_included_previously'}


type_grouping = {
'UnprotectedBody' : ['run_over', 'fall__motorcycle'],
'ShellProtected' : ['lateral_collision','frontal_lateral_collision','rear_end_collision','frontal_collision','multiple_rear_end_collision'],
'Stability&Internal ' : ['fall_inside_vehicle','overturning'],
'Environmental&Static':['crash_into_animal_on_road','crash_into_stationary','run_off_with_crash_or_collision','run_off_not_included_previously','run_off_with_overturning'],
'other':['unknown','other_types']}

type_grouping_criteria ="""

1. The "Unprotected Body" Group (Critical Risk)Total Count: 1,357
In these incidents, there is no vehicle structure between the victim and the force of impact.
Run Over (885): Direct vehicle-to-pedestrian/cyclist impact. This is the #1 predictor of fatalities in urban datasets.
Fall - Motorcycle (472): Direct impact of a rider with the pavement. Given your 76k+ motorcycles, this is a high-probability injury trigger.
Model Role: Use this as your primary indicator for "Serious Injury" or "Hospitalization."
2. The "Shell-Protected" Group (Volume Risk)Total Count: 3,820
These are vehicle-to-vehicle collisions where the occupants are inside a metal cage (Car, SUV, Van).
Lateral Collision (1,826): High risk for side-impact injuries (intrusion).
Frontal-Lateral (1,235): Significant energy transfer, often involving engine-block displacement.
Rear-End (1,715): The primary driver of "Slight" injuries (whiplash).
Frontal (147): Though low in count, these carry the highest kinetic energy ($KE = \frac{1}{2}mv^2$).
Model Role: Use these to predict injury volume rather than individual severity.
3. The "Stability & Internal" Group (Targeted Risk)Total Count: 427
These injuries are caused by the movement of the vehicle itself rather than a crash with an external object.
Fall Inside Vehicle (402): Specifically predicts injuries for bus and tram passengers.
Overturning (8) & Run-off with Overturning (4): Extremely high severity for the few people involved due to the "centrifuge" effect on the body.
Model Role: These are excellent for predicting non-collision injuries, specifically for public transit and high-center-of-gravity vehicles (SUVs/Trucks).
4. The "Environmental & Static" Group (Incidental Risk)Total Count: 884
These involve hitting objects or animals.
Crash into Stationary (664): Injury depends entirely on speed.
Crash into Animal (12): High risk of glass/windshield-related injuries.
Run-off Road (15): Often results in "Property Damage Only" unless a secondary collision occurs.
Model Role: These serve as your baseline or "control" group for the model.


"""
