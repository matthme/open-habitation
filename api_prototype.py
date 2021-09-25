import requests
from pyproj import Transformer

def get_production_info(street, nr, zipcode, city):
    searchText = street + " " + str(nr) + ", " + str(zipcode) + " " + city
    url = "https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.bfe.elektrizitaetsproduktionsanlagen&searchText=%s&searchField=address&contains=true" %(searchText)
    return requests.get(url)

def get_sub_category(response):
    return response.json()["results"][0]["attributes"]["sub_category_en"]

def get_total_power(response):
    return response.json()["results"][0]["attributes"]["total_power"]

def yearly_production_old(street, nr, zipcode, city):
    try:
        response = get_production_info(street, nr, zipcode, city)
    except Exception:
        print("API not available")
        return 0

    try:
        response_json = response.json()
    except Exception:
        print("Response could not be converted to json.")

    try:
        sub_category = get_sub_category(response)
    except KeyError:
        sub_category = "unknown"

    try:
        total_power = get_total_power(response)
        total_power = float(total_power[:-3])  # TODO: consider the unity
    except KeyError:
        total_power = 0


    if sub_category == "Photovoltaic":


        yearly_production = total_power*1000
    elif sub_category == "Wind":
        yearly_production = total_power*3600
    else:
        yearly_production = -1

    return yearly_production

def get_pv_gis_data(coordinate_x, coordinate_y):
    transformer = Transformer.from_crs('EPSG:21781', 'EPSG:4326')  # transformer from LV03 to wgs84
    coordinate_wgs84 = transformer.transform(coordinate_x, coordinate_y)
    lat = coordinate_wgs84[0]
    lon = coordinate_wgs84[1]
    peakpower = 1
    loss = 14
    mountingplace = 'free'
    angle = 35
    aspect = 60

    url = 'https://re.jrc.ec.europa.eu/api/PVcalc?' +\
          'lat=' + str(lat) +\
          '&lon=' + str(lon) +\
          '&peakpower=' + str(peakpower) +\
          '&loss=' + str(loss) +\
          '&mountingplace=' + mountingplace +\
          '&angle=' + str(angle) +\
          '&aspect=' + str(aspect) + \
          '&outputformat=json'

    return(requests.get(url).json()['outputs']['totals']['fixed']['E_y'])

def yearly_production(street, nr, zipcode, city):
    try:
        response = get_production_info(street, nr, zipcode, city)
    except Exception:
        print("API not available")
        return 0

    try:
        sub_category = get_sub_category(response)
    except KeyError:
        sub_category = "unknown"

    if sub_category == "Photovoltaic":
        coordinate_x = response.json()['results'][0]['geometry']['x']
        coordinate_y = response.json()['results'][0]['geometry']['y']
        return get_pv_gis_data(coordinate_x, coordinate_y)
    else:
        return 'No Photovoltaic found.'

# test
street = 'Hauptstrasse'
nr = 82
zipcode = 4558
city = 'Hersiwil'

yearly_production(street, nr, zipcode, city)

