#%% TODO:
import math
from BaseQueue import BaseQueue

class MG1Queue(BaseQueue):
    """
    this class is for MG1Queue, a child of BaseQueue
    """

    #constructor for MG1Queue class
    def __init__(self, lamda, mu, sigma = 0.0):
        """
        :param lamda: arrival rate
        :type lamda: either a single value, or a tuple
        :param mu: service rate
        :type mu: double
        :param sigma: process capability ratio
        :type sigma: double
        """

        # using super() to allow MG1Queue to inherit methods and properties of BaseQueue
        super().__init__(lamda, mu)

        # initialize remaining attributes
        self._sigma = sigma

    #string representation method
    def __str__(self):
        """
        :return: returns a string
        :rtype: string
        """

        # using f strings to return the formatted string
        string = (f'MG1Queue instance at {id(self)}:\n'
                  f'lamda:{self.lamda}\n'
                  f'mu:{self.mu}\n'
                  f'P0:{self.p0}\n'
                  f'Lq:{self.lq}\n'
                  f'L:{self.l}\n'
                  f'Wq:{self.wq}\n'
                  f'W:{self.w}\n'
                  f'sigma_s:{self.sigma}\n')

        return string

    # calculating p0 and lq method
    def calc_metrics(self):
        """
        :return: returns calculated p0 and lq values, if queue is valid and feasible
        :rtype: double and double
        """

        # first let's check for validity and feasibility, if not, return math.nan for both values

        if self.is_valid() == False or self.is_feasible() == False:
            self._lq = math.nan
            self._p0 = math.nan
            self.recalc_needed = False
            return

        else:  # calulating p0 and lq for MG1Queue

            self._p0 = 1 - self.ro #calculating p0

            self._lq = ((self.ro **  2) + ((self.lamda ** 2) * (self.sigma ** 2))) / (2 * (1 - self.ro))


            self.recalc_needed = False  # recalc_needed is always set to false at the end of calc_metrics

    #checking validity
    def is_valid(self):
        """
        :return: returns True if queue is valid, False if not
        :rtype: boolean
        """

        # lamda and mu must be greater than 0 in order for the queue to be valid
        if self.lamda <= 0 or self.mu <= 0 or self.sigma < 0: #added validity test for sigma
            return False

        else:
            return True

    #getter and setter for sigma
    @property
    def sigma(self): #getter
        """
        :return: returns a sigma
        :rtype: double
        """

        #TODO: idk if I need anything else here for this getter

        return self._sigma

    @sigma.setter
    def sigma(self,sigma): #setter
        """
        :return: returns the changed value of sigma
        :rtype: double
        """

        if self._sigma > 0:
            self._sigma = sigma
            #TODO: we might need a recalc_needed == True here
        else:
            self._sigma = math.nan