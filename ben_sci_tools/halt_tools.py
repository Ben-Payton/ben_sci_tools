from .process_data import g16_optfreq

def get_hind_rot_corrected_gibbs(file_path:str) -> float:
    """ gets the gibbs free energy with the hindered rotor correction if available from the specified file path in kcal/mol
    
    Parameters:
    -----------
    file_path (str): the relative path to a file

    Returns
    -------
    (float): The hindered rotor corrected gibbs free energy of the molecule in kcal/mol
    """
    file = g16_optfreq(file_path)
    file.parse_outfile()
    Vib_data = file.vibrational_thermal_contributions
    if "internal_rot." in Vib_data["Thermal_Energy"][1][0]:
        fake_gibbs = file.sum_of_electronic_and_thermal_free_energies
        fake_entropy_correction = (Vib_data["S"][0][1]/1000)/627.509
        gibbs_min = (fake_gibbs - file.thermal_correction_to_energy) - fake_entropy_correction
        true_gibbs_corr = (Vib_data["Thermal_Energy"][1][1] - 627.15*(Vib_data["S"][1][1]/1000))/627.509
        return (gibbs_min + true_gibbs_corr) * 627.509 
    return file.sum_of_electronic_and_thermal_free_energies * 627.509 


def get_uncorrected_gibbs(file_path:str):

    file = g16_optfreq(file_path)
    file.parse_outfile()
    return file.sum_of_electronic_and_thermal_free_energies * 627.509 

def sum_uncorrected_g(file_paths:tuple[str]) -> float:
    acc = 0
    for file in file_paths:
        acc = acc + get_uncorrected_gibbs(file)
    return acc



def sum_corrected_g(file_paths:tuple[str]) -> float:
    """finds the sum of the gibbs free energy of all items in a tuple in kcal/mol
    
    Parameters
    ----------
    file_paths (tuple[str]): a tuple containing the file_paths
    
    Returns
    -------
    (float): the sum of the hindered rotor corrected gibbs free energy of the files in kcal/mol"""
    acc = 0
    for file in file_paths:
        acc = acc + get_hind_rot_corrected_gibbs(file)
    return acc

def get_delta_g(reactants:tuple[str],products:tuple[str]) -> float:
    """finds the delta g of products - reactants in kcal/mol
    
    Parameters
    ----------
    reactants (tuple[str]): a tuple of the reactants files paths
    products (tuple[str]): a tuple of the products files paths

    Returns
    -------
    (float): the delta g of products - reactants in kcal/mol
    """
    return sum_corrected_g(products) - sum_corrected_g(reactants)

def get_uncorrected_delta_g(reactants:tuple[str],products:tuple[str]) -> float:
    return sum_uncorrected_g(products) - sum_uncorrected_g(reactants)

def delta_g_to_points(delta_gs:list[float],start:float = 0.0) -> list[float]:
    """converts a list of delta Gs to a list of points which represent relative free energies in kcal/mol
    
    Parameters
    ----------
    delta_gs (list[float]): a list of delta gs in kcal/mol
    start (float): a Starting point for the first relative free energy in kcal/mol, defaults to 0

    Returns
    -------
    (list[float]): the list of relative free energy points in kcal/mol
    """

    new_list = [start]
    for delta_g in delta_gs:
        new_list.append(delta_g + new_list[-1])
    return new_list

def points_to_deltag(points_list:list[float]) -> list[float]:
    """converts a list of relative gibbs free energies to a list of delta Gs in kcal/mol
    
    Parameters
    ----------
    delta_gs (list[float]): a list of relatives free energies in kcal/mol

    Returns
    -------
    (list[float]): the list of relative free energy points in kcal/mol
    """
    return [points_list[index+1] - value for index,value in points_list[:-1]]