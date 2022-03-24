#%% TODO: utilization
#TODO: not verified functions: valid, feasible, lamda, mu,
import math
class BaseQueue:

    """
    the base class that is imported by the other classes in this project
    """

    #first we need a public constructor for our class
    def __init__(self, lamda, mu):
        """
        :param lamda: arrival rate
        :type lamda: either a single value, or a tuple
        :param mu: service rate
        :type mu: double
        :return:
        :rtype:
        """

        # this is checking to make sure that the lamda provided is a valid lamda
        if self.simplify_lamda(lamda) > 0:
            self.lamda = lamda

        # if not, we set the lamda value to nan
        else:
            self.lamda = math.nan

        # if mu is greater than 0, then we provide the proper mu
        if mu > 0:
            self._mu = mu

        # if not then we provide nan
        else:
            self._mu = math.nan

        if type(mu) == str:
            self._mu = math.nan

        # we need to make sure that recalc needed is established as True so it goes through calc_metrics
        self.recalc_needed = True

    #string representation method
    def __str__(self):
        """
        :return: returns a string
        :rtype: string
        """

        #using f strings to return the formatted string
        string = (f'BaseQueue instance at {id(self)}:\n' 
                f'lamda:{self.lamda}\n'
                f'mu:{self.mu}\n'
                f'P0:{self.p0}\n'
                f'Lq:{self.lq}\n'
                f'L:{self.l}\n'
                f'Wq:{self.wq}\n'
                f'W:{self.w}\n'
                f'R:{self.r}\n'
                f'Ro:{self.ro}\n')

        return string

    #Calculating p0 and lq method
    def calc_metrics(self):
        """
        :return: None for abstract method; math.nan for BaseQueue
        :rtype: depends
        """

        #lq and p0 are set to math.nan for BaseQueue
        self._lq = math.nan
        self._p0 = math.nan

        #last action of calc_metrics is to set recalc_needed to False
        self.recalc_needed = False

    #checking validity
    def is_valid(self):
        """
        :return: returns True if queue is valid, False if not
        :rtype: boolean
        """

        #lamda and mu must be greater than 0 in order for the queue to be valid
        # if self.lamda <= 0 or self.mu <= 0:
        #     return False
        # else:
        #     return True

        if self.lamda > 0:
            if self.mu > 0:
                return True
            else:
                return False
        else:
            return False

    #checking feasibility
    def is_feasible(self):
        """
        :return: returns True if queue is feasible, False if not
        :rtype: boolean
        """

        #checking feasibility
        if self.is_valid() == True: #first check if queue is valid
            if self.lamda / self.mu < 1: #feasibility calculation
                return True

            else:
                return False

        else:
            return False

    #simplifying lamda
    def simplify_lamda(self,lamda):
        """
        :param lamda: arrival rate
        :type lamda: either a single value, or a tuple
        :return: a simplified version of lamda
        :rtype: double
        """

        #test to see if lamda is a tuple
        if type(lamda) == str:
            return math.nan

        count = 0
        if type(lamda) == tuple:
            for elements in lamda:
                if elements < 0:
                    count = count + 1
                    if count > 0:
                        return math.nan
                    else:
                        return(sum(lamda))
            #return sum(lamda) #return sum of lamda if it is a tuple

        else:
            return lamda #return lamda if not a tuple

    #getter and setter methods for lamda:
    @property
    def lamda(self): #getter
        """
        :return: returns lamda
        :rtype: double
        """

        #TODO: Do I need this stuff? We can check with the test code when it is provided.
        #check the type of lamda
        if type(self._lamda) == tuple:

            return self.simplify_lamda(self._lamda) #calls simplify_lamda function to return summed tuple value

        else: #returns just lamda if not a tuple
            return self._lamda

    @lamda.setter
    def lamda(self,lamda): #setter
        """
        :return: changed lamda value
        :rtype: double
        """

        #TODO: recalc might be needed to set to True
        # TODO: Do I need this stuff? We can check with the test code when it is provided.
        #checks that the mutated lamda is valid, return math.nan if not
        # if self.lamda > 0:
        #     if self.simplify_lamda(lamda) > 0:
        #         self.lamda = lamda
        #     else:
        #         self._lamda = math.nan
        # else:
        #     self._lamda = math.nan

        if self.simplify_lamda(lamda) > 0:
            self._lamda = lamda

        #if not, set mutated lamda to nan
        else:
            self._lamda = math.nan

    #getting and setter methods for mu:
    @property
    def mu(self): #getter
        """
        :return: returns mu
        :rtype: double
        """

        return self._mu

    @mu.setter
    def mu(self,mu): #setter
        """
        :return: changed mu value
        :rtype: double
        """

        # TODO: recalc might be needed to set to True
        # TODO: Do I need this stuff? We can check with the test code when it is provided.
        #checks that the mutated mu is valid
        if self._mu > 0:
            self._mu = mu

        else:
            self._mu = math.nan

    #getter methods for the rest of the variables:
    @property
    def lq(self): #lq getter
        """
        :return: returns lq (average number of priority class k cust.)
                 from calc_metrics
        :rtype: double
        """

        #this is needed because calc_meterics calculates lq
        if self.recalc_needed == True:
            self.calc_metrics()
            return self._lq

        # if not, then calc metrics has already been ran and we return the corresponding lq value
        else:
            return self._lq

    @property
    def p0(self): #p0 getter
        """
        :return: returns p0 from calc_metrics
        :rtype: double
        """

        #this is needed because calc_metrics calculates p0
        if self.recalc_needed == True:
            self.calc_metrics()
            return self._p0

        #if not, then calc metrics has already been ran and we return the corresponding p0 value
        else:
            return self._p0

    @property
    def l(self): #l getter
        """
        :return: returns l
        :rtype: double
        """

        self._l = self.lq + self.lamda / self.mu #calcuating lq value to return
        return self._l

    @property
    def r(self): #r getter
        """
        :return: returns r from littles_law
        :rtype: double
        """

        self._r = self.lamda/self.mu #calcualting r value to return
        return self._r

    @property
    def ro(self): #ro getter
        """
        :return: returns ro from littles_law
        :rtype: double
        """

        self._ro = self.lamda/self.mu #calculating ro value to return
        return self._ro

    @property
    def w(self): #w getter
        """
        :return: returns w from littles law
        :rtype: double
        """

        self._w = (self.lq + self.r) / self.lamda #calculating w value to return #TODO: I might need to check this calculation
        return self._w

    @property
    def wq(self): #wq getter
        """
        :return: returns wq from littles law
        :rtype: double
        """

        self._wq = self.lq / self.lamda #calculating wq value to return
        return self._wq

    @property #TODO: idk if I need this getter or not...
    def utilization(self): #utilization getter
        """
        :return: returns utilization
        :rtype: double
        """

        return self.utilization