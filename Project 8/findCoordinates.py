import pandas as pd
import requests
import math

def findCoordinates(address: list, key = None):
    """
    :param address: list of addresses
    :type address: list or Pandas.Series
    :param key: None/personal API key
    :type key: None/string
    :return: dataframe containing: lat, lng, address, and status_code
    :rtype: dataframe
    """

    #verify that the address given is a list or pandas.Series
    if type(address) != list:
        return None

    #set a limit s.t the number of coordinate sets/addresses returned by query is restricted
    limit = 1

    #placeholder variables for the final df to be returned
    lat = list()
    lng = list()
    addy = list()
    status_code = list()

    #getting the total number of addresses provided
    address_length = len(address)

    #for loop that loops over all addresses in order to run query
    for i in range(0, address_length):

        #if key is None, then use personal API key
        if key == None:
            key = 'YTOeyagUTcXydzfW2Pvr0CTWQfKQRPbw'

        #constructing url via f strings of geocode
        url = f'https://api.tomtom.com/search/2/geocode/{address[i]}.json?&limit={limit}/&key={key}'

        #replacing certain aspects of url to create the query
        query = url.replace(' ', '%20')
        query = query.replace(',', '%2C')
        query = query.replace('#', '%23')

        # execute API with request package
        r = requests.get(query)
        sc = r.status_code #gets the status code from the API
        js = r.json()  # gets the contents from the API and calls it js

        #if statement, resulting df depends on value for status code
        if sc != 200: #if status code is not 200, then the query is unsuccessful so the resulting values are:
            lat.append(math.nan)
            lng.append(math.nan)
            addy.append(address[i])
            status_code.append(sc)

        else: #if status code is 200, then the query is successful and we proceed

            if 'entryPoints' in js['results'][0]: #if the API results contain entryPoints
                lat.append(((((js['results'][0])).get('entryPoints')[0]).get('position')).get('lat')) #gets lat of the addresses, given from the API
                lng.append(((((js['results'][0])).get('entryPoints')[0]).get('position')).get('lon'))  # gets lng of the addresses, given from the API
                addy.append(((js['results'][0]).get('address')).get('freeformAddress'))
                status_code.append(sc)

            else: #if API results do not contain entryPoints
                lat.append(((js['results'][0]).get('position')).get('lat')) #gets lat of the addresses, given from the API
                lng.append(((js['results'][0]).get('position')).get('lon')) #gets lng of the addresses, given from the API
                addy.append(((js['results'][0]).get('address')).get('freeformAddress'))
                status_code.append(sc)

    #resulting dictionary that will be converted to a df
    result_dict = {'lat': lat,
                   'lng': lng,
                   'address': addy,
                   'status_code': status_code}

    #converting dictionary to a df
    df = pd.DataFrame(result_dict)

    return df