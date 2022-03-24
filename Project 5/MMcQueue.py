#%% #TODO:
import math
from BaseQueue import BaseQueue

class MMcQueue(BaseQueue):
    """
    this class is for MMcQueues, a child class to the BaseQueue class
    """

    # constructor for MMcQueue class
    def __init__(self, lamda, mu, c = 1):
        """
        :param lamda: arrival rate
        :type lamda: either a single value, or a tuple
        :param mu: service rate
        :type mu: double
        :param c: number of servers
        :type c: int
        """

        #using super() to allow MMcQueue to inherit methods and properties of BaseQueue
        super().__init__(lamda, mu)

        #initialize remaining attributes
        self._c = c

    # string representation method
    def __str__(self): #TODO: I can use inheritance for this
        """
        :return: returns a string
        :rtype: string
        """

        # using f strings to return the formatted string
        string = (f'MMcQueue instance at {id(self)}:\n'
                  f'lamda:{self.lamda}\n'
                  f'mu:{self.mu}\n'
                  f'c:{self.c}\n'
                  f'P0:{self.p0}\n'
                  f'Lq:{self.lq}\n'
                  f'L:{self.l}\n'
                  f'Wq:{self.wq}\n'
                  f'W:{self.w}\n'
                  f'R:{self.r}\n'
                  f'Ro:{self.ro}\n')

        return string

    #calculating p0 and lq method
    def calc_metrics(self):
        """
        :return: returns calculated p0 and lq values, if queue is valid and feasible
        :rtype: double and double
        """

        #first let's check for validity and feasibility, if not, return math.nan for both values

        if self.is_valid() == False or self.is_feasible() == False:
            self._lq = math.nan
            self._p0 = math.nan
            self.recalc_needed = False
            return

        else: #calulating p0 and lq

            #calculating p0 using a for loop
            term1 = 0
            for n in range(0, self.c):
                term1 = term1 + ((self.r ** n) / (math.factorial(n)))

            term2 = (self.r ** self.c) / (math.factorial(self.c) * (1 - self.ro))

            self._p0 = abs(1 / (term1 + term2))  # we want positive probability

            # now calculate lq
            num = ((self.r ** self.c) * self.ro)

            den = (math.factorial(self.c) * ((1 - self.ro) ** 2))

            self._lq = (self._p0 * num) / den

            self.recalc_needed = False #recalc_needed is always set to false at the end of calc_metrics

    #checking feasibility
    def is_feasible(self):
        """
        :return: returns True if queue is feasible, False if not
        :rtype: boolean
        """

        # checking feasibility
        if self.is_valid() == True:  # first check if queue is valid
            if self.lamda / (self.mu * self.c) < 1:  # feasibility calculation- added c element
                return True

            else:
                return False

        else:
            return False

    #checking validity
    def is_valid(self):
        """
        :return: returns True if queue is valid, False if not
        :rtype: boolean
        """

        #addition of if statement for checking if c is valid:
        if self.c <= 0:
            return False

        #lamda and mu must be greater than 0 in order for the queue to be valid
        if self.lamda <= 0 or self.mu <= 0:
            return False

        else:
            return True

    #getter and setter methods for c:
    @property
    def c(self): #c getter
        """
        :return: returns c
        :rtype: int
        """
        return self._c

    @c.setter
    def c(self,c): #c setter
        """
        :return: changed c value
        :rtype: int
        """

        if c >= 1:
            self._c = c

        else:
            self._c = math.nan

    #getter methods for r and ro to make calc_metrics calculations nicer on the eyes
    @property
    def r(self):  #r getter
        """
        :return: returns r from littles_law
        :rtype: double
        """

        self._r = self.lamda / self.mu  # calcualting r value to return
        return self._r

    @property
    def ro(self):  #ro getter
        """
        :return: returns ro from littles_law
        :rtype: double
        """

        self._ro = self.lamda / (self.mu * self.c) # calculating ro value to return
        return self._ro

    #getter methods for p0 and lq
    @property
    def lq(self):  # lq getter
        """
        :return: returns lq (average number of priority class k cust.)
                 from calc_metrics
        :rtype: double
        """

        # this is needed because calc_meterics calculates lq
        if self.recalc_needed == True:
            self.calc_metrics()
            return self._lq

        # if not, then calc metrics has already been ran and we return the corresponding lq value
        else:
            return self._lq

    @property
    def p0(self):  # p0 getter
        """
        :return: returns p0 from calc_metrics
        :rtype: double
        """

        # this is needed because calc_metrics calculates p0
        if self.recalc_needed == True:
            self.calc_metrics()
            return self._p0

        # if not, then calc metrics has already been ran and we return the corresponding p0 value
        else:
            return self._p0