import math
import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import json
import pandas as pd

def utmToLatLng(zone, easting, northing, northernHemisphere=True):
    
   
    
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
        if '¡' or 'Ã¯'or 'ï'or 'Ã\xad'or 'í' in nova:
            renova = nova.replace('¡', 'i').replace('Ã¯', 'i').replace('ï', 'i').\
            replace('Ã\xad', 'i').replace('í', 'i')
        else:
            renova = nova
        ###Lletra o
        if '\x95' or 'Ã³' or '¢' or 'ã³'or 'Ã²' or 'ò' in renova:
            trinova = renova.replace('\x95', 'o').replace('Ã³', 'o')\
            .replace('¢', 'o').replace('ã³', 'o').replace('Ã²', 'o').replace('ò', 'o')
        else:
            trinova = renova

        if '¢' in trinova:

            quatrinova = trinova.replace('¢', 'o')
        else:
            quatrinova = trinova

        ###lletra e
        if '\x82' or 'Ã©' or 'é' or 'è'or 'Ãš' or '\x8a' or 'č' in quatrinova:
            cinquinova = quatrinova.replace('\x82', 'e').replace('Ã©', 'e').replace('é', 'e').replace('è', 'e').\
            replace('Ãš', 'e').replace('\x8a', 'e').replace('č','e')
        else:
            cinquinova = quatrinova

        if '\x85' or 'Ã\xa0'in cinquinova:
            sixinova = cinquinova.replace('\x85', 'a').replace('Ã\xa0', 'a').replace('à', 'a')
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

    if it == 'Alcoholemia':
        it = 'DrunkDriving'
    if it == 'Calçada en mal estat':
        it = 'Road_damaged'
    if it == 'Drogues o medicaments':
        it = 'DUI'
    if it == 'Estat de la senyalitzacio':
        it = 'Signals_damaged'
    if it == 'Exces de velocitat o inadequada':
        it = 'Speeding'
    if it == 'Factors meteorologics':
        it = 'Weather'
    if it == 'Objectes o animals a la calçada':
        it = 'Objects or animals on the road'
    if it == 'No hi ha causa mediata':
        it = 'No mediate cause'


    return it

##transalting to catalan

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

def ped_to_angles(it):
    if it == 'Desconegut':
        it = 'unknown'
    if it == 'Creuar per fora pas de vianants':
        it = 'Crossing outside ped crossing'
    if it == 'Desobeir el senyal del semafor':
        it = 'Disobey the traffic light signal'
    if it == 'Transitar a peu per la calçada':
        it = 'Walk on the road'
    if it == 'Altres':
        it = 'Other'
    if it == 'Desobeir altres senyals':
        it = 'Disobey other signals'
    if it == 'No es causa del  vianant':
        it = 'No peds fault'


    return it


def setmana_a_angles(it):
    if it == 'Dilluns':
        it = 'Monday'
    if it == 'Dimarts':
        it = 'Tuesday'
    if it == 'Dimecres':
        it = 'Wednesday'
    if it == 'Dijous':
        it = 'Thursday'
    if it == 'Divendres':
        it = 'Friday'
    if it == 'Dissabte':
        it = 'Saturday'
    if it == 'Diumenge':
        it = 'Sunday'

    return it


def mes_a_angles(it):
    if it == 'Gener':
        it = 'January'
    if it == 'Febrer':
        it = 'February'
    if it == 'Març':
        it = 'March'
    if it == 'Abril':
        it = 'April'
    if it == 'Maig':
        it = 'May'
    if it == 'Juny':
        it = 'June'
    if it == 'Juliol':
        it = 'July'
    if it == 'Agost':
        it = 'August'
    if it == 'Setembre':
        it = 'September'
    if it == 'Octubre':
        it = 'October'
    if it == 'Novembre':
        it = 'November'
    if it == 'Desembre':
        it = 'December'

    return it

def mes_english_number(it):
    if it == 'January':
        it = '01'
    if it == 'February':
        it = '02'
    if it == 'March':
        it = '03'
    if it == 'April':
        it = '04'
    if it == 'May':
        it = '05'
    if it == 'June':
        it = '06'
    if it == 'July':
        it = '07'
    if it == 'August':
        it = '08'
    if it == 'September':
        it = '09'
    if it == 'October':
        it = '10'
    if it == 'November':
        it = '11'
    if it == 'December':
        it = '12'

    return it

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

    if 'A' in license:
        license = 'motorbike_license'
    elif 'BTP' in license:
        license = 'taxis_ambulances_license'
    elif 'B' in license:

        license = 'regular_license'
    elif 'D' in license:
        license = 'bus_license'
    elif 'C' in license:
        license = 'van_license'

    return license

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

def getting_next_day(date):
    """Adds a day to the date"""
    return (datetime.strptime(date, '%Y-%m-%d')+ timedelta(days=1)).strftime("%Y-%m-%d")
def getting_daily_weather(date):
    
    """Scrape the weather info fro barcelona during the date"""
    
    url = 'https://darksky.net/details/41.4003,2.1596/'+date+'/us12/en'
    respo = requests.get(url)
    #print('Status Code: ', respo.status_code)
    soup = BeautifulSoup(respo.content, 'lxml')
    p_s  = str(soup.find_all('script')[1])
    s_s = p_s[p_s.find('['):p_s.find(']')+1]
    jdata = json.loads(s_s)
    df = pd.DataFrame(columns=[key for key in jdata[0].keys()])

    for x in range(0,len(jdata)):
    
        df = df.append(jdata[x]
          , ignore_index=True)
    df['time'] = df['time'].apply(lambda x: (datetime.fromtimestamp(x)+ timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S'))
    
    return df

#mapping_vehicles


map_vehicles={'Motocicleta': 'motorcycle',
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
'Tractor camió': 'Tractor camió-truck',
'Tot terreny':'suv',
'Quadricicle < 75 cc':'quadricycle under 75cc',
'Desconegut':'unknown',
'Microbus <= 17': 'minibus <17 pass',
'Veh. mobilitat personal amb motor': 'personal motor vehicles',
'Veh. mobilitat personal sense motor':'personal non-motor vehicles',
'Microbús <= 17': 'minibus <17 pass',
'Carro':'wagon',
'Pick-up':'van',
"Maquinŕria d'obres i serveis":'construction machinery',
"Maquinària d'obres i serveis":'construction machinery',
'Ambulŕncia': 'ambulance'}

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