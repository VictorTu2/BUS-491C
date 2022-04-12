#%%
import pandas as pd
import re
#%%
def extractCoordinates(dat):
    """
    :param dat: dataframe (csv file)
    :type dat: string
    :return: dataframe with 3 columns
    :rtype: dataframe
    """

    #reading csv file
    df = pd.read_csv(dat)

    #checking to make sure station and coordinates exist in the df
    if df.columns[0] != 'station':
        return -1
    elif df.columns[1] != 'coordinates':
        return -2

    #getting the number of stations
    n_stat = len(df['station']) #we have 24 stations

    # dictionary to store values
    new_dict = {}

    # converting dictionary to dataframe
    new_df = pd.DataFrame(new_dict)

    # populating station column
    new_df['station'] = range(1, n_stat + 1)

    #creaing lists for lat and lon
    lat = list()
    lon = list()

    #foor loop that pulls the lat and lon of each station
    for i in range(0,n_stat):

        pattern = re.compile(r'^\(((?P<lat>-*\d+\.*\d*), *(?P<lon>-*\d+\.*\d*))\)$') #pulls lat and lon values

        result = pattern.search(df['coordinates'][i]) #uses the pattern from above to search through the coordinates column

        #if statement to convert lat and lon to numeric value
        if result != None:

            lat.append(float(result.group('lat')))
            lon.append(float(result.group('lon')))

        else:
            print('None') #print None if pattern.search returns a None

    #converting both lat and lon lists to dataframes
    lat = pd.DataFrame(lat)
    lon = pd.DataFrame(lon)

    #populating lat and lon columns
    new_df['lat'] = lat
    new_df['lon'] = lon

    # moving index 1 up (getting rid of 0th index)
    new_df.index = range(1, n_stat + 1)

    return new_df

#%%
extractCoordinates('coordinates.csv')

