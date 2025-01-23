import numpy as np

def sinterpolate(x:np.array,y:np.array,num_points:int=10):
    """ interpolates between two points by 1/4 of a wavelength useful for reaction coordinates

    Parameters
    ----------

    x : an array of size 2 of x values of the two points

    y : an array of size 2 of y values of the two points

    num_points (int): the number of points in the final interpolation

    Returns
    -------

    (final_x,final_y) : x and y values of the interpolation
    """
    final_x = np.linspace(x[0],x[1],num_points)
    ydiff = y[1]-y[0]
    xdiff = x[1]-x[0]
    amplitude = ydiff/2
    frequency = np.pi/xdiff
    phase = -1*((np.pi/2)+((x[0]*np.pi)/xdiff))
    yshift = y[0] + ydiff/2
    final_y = amplitude* np.sin(frequency*final_x+phase)+yshift
    return final_x,final_y

def multi_sinterpolate(x:np.array,y:np.array,num_points:int=10):
    """ does a sinterpolation between each point in the x ,y arrays
    
    Parameters
    ----------

    x : an array of x values for a set of points

    y : an array of y values for a set of points

    num_points int : The number of points between each inital set of points
    
    Returns
    -------

    (final_x,final_y) : x and y values of the interpolation
    """
    final_x =[]
    final_y = []
    for index, value in enumerate(x[:-1]):
        tempx , tempy = sinterpolate(x[index:index+2],y[index:index+2],num_points)
        for index,value in enumerate(tempx[:-1]):
            final_x.append(tempx[index])
            final_y.append(tempy[index])
    final_x.append(x[-1])
    final_y.append(y[-1])
    return final_x,final_y 