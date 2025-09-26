def md_calc_concentration(num_solute:int,num_solvent:int,molar_volume_solvent:float=18.01528) -> float:
    """Roughly calculates the concentration of an MD simulation in molarity
    
    Parameters
    ----------
    num_solute (int): the number of solute atoms or molecules
    
    num_solvent (int): the number of solvent atoms or molecules
    
    molar_volume_solvent (float): the molar volume of a solvent defaults to water at stp
    
    Returns
    -------
    
    float: the molar concentration of the solute in solution"""
    return 1000*(num_solute/num_solvent)/molar_volume_solvent

def md_calc_num_solvent(num_solute:int,molarity_target:float,molar_volume_solvent:float=18.01528) -> int:
    """Roughly calculates the number of solvent molecules for a target concentration
    
    Parameters
    ----------
    num_solute (int): the number of solute atoms or molecules
    
    molarity_target (float): The target molarity
    
    molar_volume_solvent (float): the molar volume of a solvent defaults to water at stp
    
    Returns
    -------
    
    int: the number of solvent molecules required for the target concentration"""
    return round((1000/molar_volume_solvent)*(num_solute/molarity_target))

def md_calc_num_solute(num_solvent:int,molarity_target:float,molar_volume_solvent=18.01528) -> int:
    """Roughly calculates the number of solute molecules for a target concentration
    
    Parameters
    ----------
    num_solvent(int): the number of solvent atoms or molecules
    
    molarity_target (float): The target molarity
    
    molar_volume_solvent (float): the molar volume of a solvent defaults to water at stp
    
    Returns
    -------
    
    int: the number of solute molecules required for the target concentration"""
    return round(molar_volume_solvent/1000)*(molarity_target*num_solvent)