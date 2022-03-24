#%% TODO:
import math
from BaseQueue import BaseQueue

class MM1Queue(BaseQueue):
    """
    this class is for MD1Queue, a child class of BaseQueue
    """

    def calc_metrics(self):
        """
        :return: returns p0 and lq values, if queue is valid and feasible
        :rtype: double and double
        """

        # first let's check for validity and feasibility, if not, return math.nan for both values

        if self.is_valid() == False or self.is_feasible() == False:
            self._lq = math.nan
            self._p0 = math.nan
            self.recalc_needed = False
            return

        else:  # calulating p0 and lq for a MD1Queue

            self._p0 = 1 - self.ro #calculating p0

            self._lq = (self.lamda ** 2) / (2 * self.mu * (self.mu - self.lamda)) #calculating lq

            self.recalc_needed = False  # recalc_needed is always set to false at the end of calc_metrics
