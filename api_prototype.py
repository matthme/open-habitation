import requests

def get_production_info(street, nr, zipcode, city):
    searchText = street + " " + str(nr) + ", " + str(zipcode) + " " + city
    url = "https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.bfe.elektrizitaetsproduktionsanlagen&searchText=%s&searchField=address&contains=true" %(searchText)
    return requests.get(url)

def get_sub_category(response):
    return response.json()["results"][0]["attributes"]["sub_category_en"]

def get_total_power(response):
    return response.json()["results"][0]["attributes"]["total_power"]

def yearly_production(street, nr, zipcode, city):
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


# test
street = 'Hauptstrasse'
nr = 82
zipcode = 4558
city = 'Hersiwil'

response = get_production_info(street, nr, zipcode, city)
get_sub_category(response)
get_total_power(response)
yearly_production = yearly_production(street, nr, zipcode, city)
print(yearly_production)

