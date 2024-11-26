from math import exp
from math import log

class first_order:
    """A class for first order equations.
    Attributes
    ----------
    k (float): the first order rate constant
    C (float): the the constant for the linearized rate equation.
    A (float): the preexponential factor
    rounding (int): The ammount to round to when giving an equation
    """

    def __init__(self,k:float,C:float,rounding:int=3) -> None:
        """A class for first order equations.
        Parameters
        ----------
        k (float): the first order rate constant
        C (float): the the constant for the linearized rate equation.
        rounding (int): The ammount to round to when giving an equation
        """
        self.k = k
        self.C = C
        self.rounding = rounding
        self.A = exp(C)
        pass

    @classmethod
    def from_two_points(cls,point1:tuple[float],point2:tuple[float]):
        """Creates a first order object from two points of format (time,value)
        
        Parameters
        ----------
        point1 (tuple[float]): the first point of (time,value)
        point2 (tuple[float]): the second point of (time,value)
        
        Returns
        -------
        first_order
        """
        time_i = point1[0] - point1[0]
        time_f = point2[0] - point1[0]
        value_i = point1[1]
        value_f = point2[1]

        future_C = log(value_i)
        future_k = (log(value_f) - future_C)/ time_f
        return cls(future_k,future_C)
    
    def value_at_time(self,time:float) -> float:
        """ returns a the expected value at a given time of an exponential function:

        Parameters
        ----------
        time (float): the time of a measurment

        Returns:
        -------
        float: The value at the specified time 
        """
        return self.A * exp(self.k*time)
    
    def val_from_initial_and_time(self,vi:float,time:float) -> float:
        """given a starting value and an amount of time it gives the final value
        Parameters
        ----------
        vi (float): starting value
        time (float): The amount of time passed
        """
        return vi * exp(self.k*time)
    
    def __str__(self) -> str:
        return f"x = {round(self.A,self.rounding)}e^({round(self.k,self.rounding)} t)"