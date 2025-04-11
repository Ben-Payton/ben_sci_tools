

def bayesian(prior:float,sensitivity:float,false_positive_rate:float,num_test:int=1) -> float:
    """ Performs a basian analysis to calculate a prior.

    Parameters
    ----------
    prior (float): the prior probability that a statement is true
    sensitivity (float): the probability that the test is positive for the subset of positive cases
    false_positive_rate (float): the probability of a false positive for the sub set of negative cases
    num_tests (int): The number of times the test us applied.

    Returns
    -------

    float: the posterior value
    """
    num_run = 1
    posterior = (prior * sensitivity)/((1-prior)*false_positive_rate+prior*sensitivity)
    while num_run < num_test:
        num_run +=1
        posterior = (posterior * sensitivity)/((1-posterior)*false_positive_rate+posterior*sensitivity)

    return posterior

def bayes_until_certain(prior:float,sensitivity:float,false_positive_rate:float,certainty:float) -> tuple[float,int]:
    """ Performs a basian analysis to calculate the number of times a test needs to be performed to reach a desired level of certainty.

    Parameters
    ----------
    prior (float): the prior probability that a statement is true
    sensitivity (float): the probability that the test is positive for the subset of positive cases
    false_positive_rate (float): the probability of a false positive for the sub set of negative cases
    certainty (float): the level of certainty you would want

    Returns
    -------

    int, float: the number of tests you would need to apply to reach the desired level of certainty, the posterior value
    """
    posterior = bayesian(prior,sensitivity,false_positive_rate)
    num_applied = 1
    while posterior<certainty:
        num_applied +=1
        posterior = bayesian(posterior,sensitivity,false_positive_rate)
    return num_applied,posterior

