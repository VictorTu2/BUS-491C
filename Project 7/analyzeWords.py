#%%
import pandas as pd
import re
import string
#%%
def analyzeWords(words):
    """
    :param words: a series of words
    :type words: Pandas.series
    :return: a dictionary of metrics:
             letter_counts- dict of counts of words beginning with each letter of the alphabet
             max_char- the number of characters of the longest word
             size_counts- a dict of counts of words consisting of 1,2,3,..., max_char characters
             oo_count- the number of words containing a double-o
             oo_words- a Pandas.Series of words containing a double-o
             words_6plus- a Pandas.Series of words containing 6 or more letters
             words_6plus_count- the number of words containing 6 or more letters
    :rtype: dict
    """

    #reading words.csv file
    df = pd.read_csv(words)

    #creating letter_counts:
    abc = list(string.ascii_lowercase) #list of the entire alphabet

    letter_counts = {} #letter_counts list that will contain all the numbers for each letter

    [letter_counts.update({abc[i]: None}) for i in range(0, len(abc))] #creating the key but not populating any numbers yet

    for letter in range(0, len(abc)): #getting the number for each letter
        count_total = sum([bool(re.search(f'^{abc[letter]}', w)) for w in df['x']])  #sum of each letter

        letter_counts[f'{abc[letter]}'] = count_total  #puts the sum into the dictionary with the correct key

    #creating max_char:
    longest_word = max(df['x'], key=len) #finding the longest word

    max_char = len(longest_word) #taking the length of the longest word

    #creating size_counts:
    size_counts = {}  #dictionary to be used

    [size_counts.update({i: 0}) for i in range(1, max_char + 1)]  #creates the keys for the dict

    length_words = [len(df['x'][w]) for w in range(0, len(df['x']))]  #getting the length of all the words

    for i in range(1, max_char + 1): #loop to populate dict
        letter_total = length_words.count(i)  # sum of each letter

        size_counts[i] = letter_total #placing the number in the correct spot

    #creating oo_count:
    oo_count = sum([bool(re.search('(oo)', w)) for w in df['x']]) #sums all words with a oo


    #creating oo_words:
    oo_words = df['x'].loc[[bool(re.search('(oo)', w)) for w in df['x']]] #displays all words with a oo

    #creating words_6plus:
    words_6_tf = [length_words[w] >= 6 for w in range(0, len(df['x']))]

    words_6plus = df['x'].loc[words_6_tf]

    #creating words_6plus_count:
    words_6_plus_count = len(words_6plus)

    #creating analyzeWords dict:
    analyzeWords = {'letter_counts': letter_counts,
                    'max_char': max_char,
                    'size_counts': size_counts,
                    'oo_count': oo_count,
                    'oo_words': oo_words,
                    'words_6plus': words_6plus,
                    'words_6plus_count': words_6_plus_count
                    }
    return analyzeWords
#%%
analyzeWords('words.csv')
