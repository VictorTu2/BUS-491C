#%%
#writing is_valid function
def is_valid(lamda, mu: float, c: int = 1):
    """
    Evaluates lamda, mu, and c to determine if the queue is valid
    :param lamda: arrival rate
    :param mu: service rate
    :param c: number of servers
    :return: if the queue is valid, False otherwise
    """

    #makes sure all of the parameters are not strings
    if type(lamda) == str or type(mu) == str or type(c) == str:
        return False

    #check if lamda is a tuple
    if type(lamda) == tuple:

        for value in lamda: #check if any of the values in lamda are negative
            if value <= 0:
                return False

        agg_lamda = sum(lamda)
        if agg_lamda < 0: #check if total lamda is positive
            return False
    else:
        if lamda <= 0: #check if lamda is positive
            return False

    #check if mu and c are valid
    if mu <= 0 or c <= 0:
        return False
    else:
        return True

#%%
#writing is_feasible function
def is_feasible(lamda, mu: float, c: int = 1):
    """
    :param lamda: arrival rate
    :param mu: service rate
    :param c: number of servers
    :return: if queue is feasible, return valid, false if otherwise
    """
    #makes sure any of the parameters are not strings
    if type(lamda) == str or type(mu) == str or type(c) == str:
        return False

    # calls is_valid function to check for parameter validity
    if is_valid(lamda,mu,c) == False:
        return False

    # check if lamda is a tuple
    if type(lamda) == tuple:

        for value in lamda: #check if values in lamda are negative
            if value < 0:
                return False

        agg_lamda = sum(lamda) #used to calculate rho

        rho = agg_lamda / (c * mu) #calculates rho

    else:
        rho = lamda / (c * mu) #calculates rho if lamda is a single value

    #testing if rho is less than 1, returns booleans
    if rho < 1:
        return True
    else:
        return False

#%%
import math
#writing calc_p0 function
def calc_p0(lamda, mu: float, c: int = 1):
    """
    :param lamda: arrival rate
    :param mu: service rate
    :param c: number of servers
    :return: if queue is valid/feasible, returns p0
             if queue is invalid, returns math.nan
             if queue is infeasible, returns math.inf
    """

    #calling is_valid
    if is_valid(lamda,mu,c ) == False:
        return math.nan

    #calling is_feasible
    if is_feasible(lamda,mu,c) == False:
        return math.inf

    # check if lamda is a tuple
    if type(lamda) != tuple:
        r = lamda / mu

        rho = r / c #calculating rho for when lamda is not a tuple

    else:
        agg_lamda = sum(list(lamda)) #lamda is a tuple, we aggregate it

        r = agg_lamda / mu

        rho = r / c #calculating rho for when lamda is a tuple

    #checking for value of c
    if c <= 1: #easy calculation because c <= 1
        p0 = abs(1 - rho) #we want positive probability
        return p0 #returns p0

    else: #more in-depth calculation becuase c > 1
        term1 = 0
        for n in range(0, c):
            term1 = term1 + ((r ** n) / (math.factorial(n)))

        term2 = (r ** c) / (math.factorial(c) * (1-rho))

        p0 = abs(1 / (term1 + term2)) #we want positive probability

        return p0 #returns p0

#%%
#writing calc_lq_mmc function
def calc_lq_mmc(lamda, mu: float, c: int = 1):
    """"
    :param lamda: arrival rate
    :param mu: service rate
    :param c: number of servers
    :return: if queue is valid/feasible, returns Lq
             if queue is invalid, returns math.nan
             if queue is infeasible, returns math.inf
    """

    # calling is_valid
    if is_valid(lamda, mu, c) == False:
        return math.nan

    # calling is_feasible
    if is_feasible(lamda, mu, c) == False:
        return math.inf

    # check if lamda is a tuple
    if type(lamda) != tuple:
        r = lamda / mu

        rho = r / c #calculating rho for when lamda is not a tuple

    else:
        lamda = sum(list(lamda))  # lamda is a tuple, we aggregate it

        r = lamda / mu

        rho = r / c #calculating rho for when lamda is a tuple

    # checking for value of c
    if c == 1:
        lq = (lamda**2) / (mu * (mu - lamda))

        return lq #return lq if c = 1

    else:
        p0 = calc_p0(lamda, mu, c) #get p0 from calc_p0 function

        #now calculate lq
        num = ((r**c)*rho)

        den = (math.factorial(c)*((1-rho)**2))

        lq = (p0 * num) / den

        return lq #return lq for values where c is not 1

#%%
#writing calc_bk_mmc function
def calc_bk_mmc(k, lamda, mu: float, c: int = 1):
    """
    :param k:
    :param lamda: arrival rate
    :param mu: service rate
    :param c: number of servers
    :return: if queue is valid/feasible, returns Bk
             if queue is invalid, returns math.nan
             if queue is infeasible, returns math.inf
    """

    #checking validity
    if is_valid(lamda, mu, c) == False:
        return math.nan

    #checking feasibility
    if is_feasible(lamda, mu, c) == False:
        return math.inf

    #check if lamda is a tuple
    if type(lamda) == tuple:
        wlamda = lamda
    else:
        wlamda = (lamda,)

    #checking values of k to make sure it is valid
    if k == 0:
        return 1

    if k > len(wlamda):
        return math.nan

    else:

        rho = [l / (c * mu) for l in wlamda[0:k]] #calculating rho through for loop

        Bk = 1-sum(rho) #calculating Bk

        return Bk

#%%
import math
#writing calc_wqk_mmc function
def calc_wqk_mmc(k, lamda, mu: float, c:int = 1):
    """
    :param k: priority class
    :param lamda: arrival rate
    :param mu: service rate
    :param c: number of servers
    :return: if queue is valid/feasible, returns Wqk
             if queue is invalid, returns math.nan
             if queue is infeasible, returns math.inf
    """

    #checking validity
    if is_valid(lamda, mu, c) == False:
        return math.nan

    #makes sure value of k is valid
    if k <= 0:
        return math.nan

    #checking feasibility
    if is_feasible(lamda, mu, c) == False:
        return math.inf

    #checking if lamda is a tuple
    if type(lamda) == tuple:
        wlamda = lamda
    else:
        wlamda = (lamda,)

    #make sure k is a valid value
    if k > len(wlamda):
        return math.nan

    else:
        lamda_agg = sum(wlamda) #used to calculate rho

        rho = lamda_agg / (c * mu ) #calculating rho

    #calculating wqk
    lq = calc_lq_mmc(lamda, mu, c) #using calc_lq_mmc function to calculate lq

    wq = lq / lamda_agg

    bk = calc_bk_mmc(k, lamda, mu, c) #using calc_bk_mmc function to calculate bk

    bk_1 = calc_bk_mmc(k-1, lamda, mu, c) #using calc_bk_mmc function to calculate bk, where is k-1

    wqk = (1-rho) * wq / (bk * bk_1) #now calculate wqk

    return wqk

#%%
import math
import numpy
#writing calc_lqk_mmc function
def calc_lqk_mmc(k, lamda, wqk, c = 1):
    """
    :param k: priority class
    :param lamda: arrival rate
    :param wqk: average waiting time
    :return: if k is less than or equal to 0 or greater than magnitude of lamda, return math.nan
             return wqk if else
    """

    #makes sure we have the correct type input for k
    if type(k) != int:
        return math.nan

    #makes sure we have the correct type input for lamda
    if type(lamda) != tuple:
        return math.nan

    if type(lamda) == tuple:
        for i in lamda: #checking elements of lamda
            if i < 0:
                return math.nan
    elif lamda <= 0:
        return math.nan

    #make sure k is proper for the function
    if k <= 0:
        return math.nan

    if k > len(lamda):
        return math.nan

    #calculating Lqk
    lamda_k = lamda[k-1]

    Lqk = lamda_k * wqk

    return Lqk
#%%
def use_littles_law(lamda, mu: float, c: int = 1,**kwargs):
    """"
    :param lamda: arrival rate
    :param mu: service rate
    :param c: number of servers (default 1)
    :param kwargs: key word0 must contain one of: lq, l, wq, w
    :return: a dictionary if queue is valid and feasible
             math.inf if queue is infeasible
             math.nan if queue is invalid
    """

    # check if queue is valid
    if is_valid(lamda, mu, c) == False:
        return math.nan

    # check if queue is feasible
    if is_feasible(lamda, mu, c) == False:
        return math.inf

    #checking if kwargs is empty
    if kwargs == {}:
        return None

    #check if lamda is a tuple
    if type(lamda) == tuple:
        #is_priority = True
        wlamda = sum(lamda)

    else:
        #is_priority = False
        wlamda = lamda

    #calculating r and ro for later
    r = wlamda / mu
    ro = wlamda / (mu * c)

    #creating results dictionary
    littles = {}

    #converting **kwargs to Lq
    if list(kwargs.keys())[0] == 'lq': #converting for lq keyword
        littles['lq'] = list(kwargs.values())[0]

    elif list(kwargs.keys())[0] == 'l': #converting for l keyword
        littles['lq'] = list(kwargs.values())[0] - r

    elif list(kwargs.keys())[0] == 'wq': #converting for wq keyword
        littles['lq'] = list(kwargs.values())[0] * wlamda

    elif list(kwargs.keys())[0] == 'w': #converting for w keyword
        littles['lq'] = list(kwargs.values())[0] * wlamda - r

    else: #if there is no keyword, return None
        return None

    #calculating L, Wq, and W using LQ; save calculated metrics in the 'littles' dictionary

    #keys for the littles dictionary
    keys = ['lq',
            'l',
            'wq',
            'w',
            'r',
            'ro']

    #values of littles dictionary
    values = [littles['lq'], #lq
              littles['lq'] + r, #l
              littles['lq'] / wlamda, #wq
              (littles['lq'] + r) / wlamda, #w TODO: check this
              wlamda / mu, #
              wlamda / (c * mu)] #ro

    #making the littles dictionary
    for key in range(len(keys)):
        littles[keys[key]] = values[key]

    #priority class
    if type(lamda) == tuple and len(lamda) > 1: #it is a class if it satisfies these conditions

        n = len(lamda)

        wqk = [calc_wqk_mmc(i, lamda, mu, c) for i in range(1,n + 1)]
        lqk = [calc_lqk_mmc(i, lamda, wqk[i-1], c) for i in range(1,n + 1)]

        littles['wqk'] = wqk #assign wqk to littles dict
        littles['lqk'] = lqk #assign lqk to littles dict

        return littles

    else: #it not a class becuase conditions were not satisfied, so just return the dictionary
        return littles