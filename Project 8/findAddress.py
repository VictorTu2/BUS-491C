#%%
import pandas as pd
import requests
import math
#%%
def findAddress(lat: tuple, lng: tuple, key = None):
    """
    :param lat: latitude portion of coordinates
    :type lat: tuple
    :param lng: longitude portion of coordinates
    :type lng: tuple
    :param key: None/personal API key
    :type key: None/string
    :return: dataframe containing two columns of contents depending on success of query
    :rtype: dataframe
    """

    #verify that the lat and lng given are tuples
    if type(lat) and type(lng) != tuple:
        return None

    #if lat and lng do not have the same lengths, the function should return None
    if len(lat) != len(lng):
        return None

    #placeholder variables for the final df to be returned
    addy = list()
    status_code = list()

    #getting the total number of lats and lngs provided
    coord_len = len(lat) #only need to get the length of one or the other, since they are the same lengths (checked above)

    # for loop that loops over all addresses in order to run query
    for i in range(0, coord_len):

        # if key is None, then use personal API key
        if key == None:
            key = 'YTOeyagUTcXydzfW2Pvr0CTWQfKQRPbw'

        #constructing url via f strings of reverse geolocation
        url = f'https://api.tomtom.com/search/2/reverseGeocode/{lat[i]}%2C{lng[i]}.json?key={key}'

        # execute API with request package
        r = requests.get(url)
        sc = r.status_code  # gets the status code from the API
        js = r.json()  # gets the contents from the API and calls it js

        #if statement, resulting df depends on value for status code
        if sc != 200:  # if status code is not 200, then the query is unsuccessful so the resulting values are:
            addy.append(math.nan)
            status_code.append(sc)

        else:  # if status code is 200, then the query is successful and we proceed
            addy.append((((js['addresses'][0]).get('address')).get('freeformAddress')))
            status_code.append(sc)

    # resulting dictionary that will be converted to a df
    result_dict = {'address': addy,
                   'status_code': status_code}

    # converting dictionary to a df
    df = pd.DataFrame(result_dict)

    return df