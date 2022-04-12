#%%
import pandas as pd
#%%
def reformatSamples(samples):
    """
    :param samples: dataframe (csv file)
    :type samples: string
    :return: dataframe of reformated samples
    :rtype: dataframe
    """

    #read csv file
    df = pd.read_csv(samples)

    #verifying that all samples have the same number of observations
    n = df.nunique()['sample'] #number of unique samples in the df

    for sample in range(2,n+1): #for loop used to check length of observations are all the same, return None if not
        if len(df[df['sample'] == sample]) != len(df[df['sample'] == sample-1]):
            return None

    #creating the new dataframe containing the restructured data

    sample_dict = {} #dictionary containing appropriate values

    n_obs = len(df[df['sample'] == 1]) #the number of observations for each sample

    for cols in range(1, n_obs+1): #for loop to create the columns
        sample_dict[f'obs.{cols}'] = list(df['diameter'][cols-1::n_obs])

    new_df = pd.DataFrame(sample_dict) #converting dict to dataframe

    new_df.index = range(1, n + 1) #shifting index up 1 to get rid of the 0

    new_df['sample'] = range(1, n + 1) #creating the sample column

    new_df = new_df[['sample', 'obs.1', 'obs.2', 'obs.3', 'obs.4','obs.5']] #reordering columns

    return new_df
#%%
reformatSamples('pistonrings.csv')


