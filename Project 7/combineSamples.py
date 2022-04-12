#%%
import pandas as pd
import math
import os
import re
#%%
def combineSamples(pattern, path = ".", control_samples = None):
    """
    :param pattern: used to determine what csv files are to be combined
    :type pattern: string
    :param path: specification of path in order for directory to be searched
    :type path: string
    :param control_samples: number of samples to be included in the control sample
    :type control_samples: int
    :return: dictionary that contains:
             -pattern (pattern argument)
             -path (path argument value)
             -control_samples (control_samples argument value)
             -files (number of files matching pattern)
             -filenames (list of filenames matching pattern)
             -samples (the samples data frame)
             -control (the control data frame)
             -test (the test data frame)
    :rtype: dict
    """

    dir_list = os.listdir(path) #list of all files in the directory

    num_boiler_csvs = [i for i in dir_list if re.search(f'{pattern}', i)] #number of boiler_csv files in the folder

    files = len(num_boiler_csvs) #total number of boiler_csv files

    if files != 0: #checking length of files

        # combining the first 9 csv files
        samples_csv_9 = pd.concat([pd.read_csv(f'{pattern}_0{i}.csv') for i in range(1, 10)])

        #combining csv files 10-25 now
        samples_csv_25 = pd.concat([pd.read_csv(f'{pattern}_{i}.csv') for i in range(10,26)])

        #combining both files
        samples = samples_csv_9.append(samples_csv_25)

        #renaming 0 column
        samples.rename(columns={"Unnamed: 0": "sample"}, inplace=True)

        #creating additional dataframes:
        control = pd.DataFrame()
        test = pd.DataFrame()

        #if statement to populate the control and test dataframes based on control_samples
        if control_samples == None:
            sample_prop = int(.6 * files)
            control = samples[samples['sample'] <= sample_prop]
            test = samples[samples['sample'] > sample_prop]
        else:
            sample_prop = control_samples
            control = samples[samples['sample'] <= sample_prop]
            test = samples[samples['sample'] > sample_prop]

        combineSamples_dict = {'pattern': pattern,
                               'path': path,
                               'control_samples': control_samples,
                               'files': num_boiler_csvs,
                               'filenames': num_boiler_csvs.sort(),
                               'control': control,
                               'test': test
                               }

        return combineSamples_dict

    else: #if files is equal to 0, do not return some parameters
        return {'pattern': pattern,
                'path': path,
                'control_samples': control_samples,
                'files': files
                }
#%%
combineSamples('boiler_sample', '.', 8)

