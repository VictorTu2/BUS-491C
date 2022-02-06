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
        if lamda <= 0:
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

        agg_lamda = sum(lamda)

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
    :return: if queue is feasible, returns p0
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

        rho = r / c

    else:
        agg_lamda = sum(list(lamda)) #lamda is a tuple, we aggregate it

        r = agg_lamda / mu

        rho = r / c

    #checking for value of c
    if c <= 1: #easy calculation because c <= 1
        return_val = abs(1 - rho) #we want positive probability
        return return_val

    else: #more in-depth calculation becuase c > 1
        term1 = 0
        for n in range(0, c ):
            term1 = term1 + ((r ** n) / (math.factorial(n)))

        term2 = (r ** c) / (math.factorial(c) * (1-rho))

        p0 = abs(1 / (term1 + term2)) #we want positive probability

        return p0

#%%
#writing calc_lq_mmc function
def calc_lq_mmc(lamda, mu: float, c: int = 1):
    """"
    :param lamda: arrival rate
    :param mu: service rate
    :param c: number of servers
    :return: if queue is feasible, returns Lq
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

        rho = r / c

    else:
        lamda = sum(list(lamda))  # lamda is a tuple, we aggregate it

        r = lamda / mu

        rho = r / c

    # checking for value of c
    if c == 1:
        lq = (lamda**2) / (mu * (mu - lamda))

        return lq

    else:
        p0 = calc_p0(lamda, mu, c)

        num = ((r**c)*rho)

        den = (math.factorial(c)*((1-rho)**2))

        lq = (p0 * num) / den

        return lq