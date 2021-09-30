import requests
from pyproj import Transformer


def get_production_info_string(searchText):
    url = "https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.bfe.elektrizitaetsproduktionsanlagen&searchText=%s&searchField=address&contains=true" % (
        searchText)
    return requests.get(url)


def get_production_info(street, nr, zipcode, city):
    searchText = street + " " + str(nr) + ", " + str(zipcode) + " " + city
    return get_production_info_string(searchText)


def get_sub_category(response_json):
    return response_json["attributes"]["sub_category_en"]


def get_pv_gis_data(coordinate_x, coordinate_y):
    # transformer from LV03 to wgs84
    transformer = Transformer.from_crs('EPSG:21781', 'EPSG:4326')
    coordinate_wgs84 = transformer.transform(coordinate_x, coordinate_y)
    lat = coordinate_wgs84[0]
    lon = coordinate_wgs84[1]
    peakpower = total_power
    loss = 14
    mountingplace = 'free'
    angle = 35
    aspect = 60

    url = 'https://re.jrc.ec.europa.eu/api/PVcalc?' + \
          'lat=' + str(lat) + \
          '&lon=' + str(lon) + \
          '&peakpower=' + str(peakpower) + \
          '&loss=' + str(loss) + \
          '&mountingplace=' + mountingplace + \
          '&angle=' + str(angle) + \
          '&aspect=' + str(aspect) + \
          '&outputformat=json'

    return (requests.get(url).json()['outputs']['totals']['fixed']['E_y'])


def yearly_production(street, nr=None, zipcode=None, city=None):
    try:
        if nr is None:
            response = get_production_info_string(street)
        else:
            response = get_production_info(street, nr, zipcode, city)
    except Exception:
        print("API not available")
        return None

    result_data = response.json()["results"]
    if len(result_data) == 0:
        return None

    try:
        sub_category = get_sub_category(result_data[0])
    except KeyError:
        sub_category = "unknown"

    if response.json()['results'][0]['geometry'] is None:
        return None

    if sub_category == "Photovoltaic":
        coordinate_x = response.json()['results'][0]['geometry']['x']
        coordinate_y = response.json()['results'][0]['geometry']['y']
        return get_pv_gis_data(coordinate_x, coordinate_y)
    else:
        return None


def calculate_rating(yearly_production=None):
    if yearly_production is None:
        return 'G'
    if yearly_production < 5000:
        return 'E'
    else:
        return 'A'


def calculate_results(searchText):
    output = {}
    output['address'] = searchText
    output['yearly_production'] = yearly_production(searchText)
    output['eco_rating'] = calculate_rating(output['yearly_production'])

    try:
        response = get_production_info_string(searchText)
        result_data = response.json()["results"]
        if len(result_data) == 0:
            # No address found
            return None
        output['category'] = get_sub_category(result_data[0])
        output['total_power'] = result_data[0]["attributes"]["total_power"]
    except:
        output['category'] = 'no data'
        output['total_power'] = -1

    return output
