# Project Description

ben-science-tools (bst) is meant to contain tools that Ben uses to streamline some of his porcesses while working on computaional chemistry.
The project currently has two main modules process_data which is used for log file or computaional chemistry output file processing and analysis, and input_file_maker which is used to generate file inputs for computational chemistry

# Documentation

## process_data

### Functions

`statp`
takes a file patern and returns the number of stationary points in each file that fits that pattern.

    Parameters
    ----------
    file_patern (str) :  a string that matches a certain string

    Returns
    -------
    a string that gives nomber of occurences and line numbers of stationary points

### Classes

`out_file_scraper`
This is a parent file scraper class meant to be altered or used for scraping log files for computations. 
    
    Attributes
    ----------
    path : str
        a path to an output file
    
    file_list : list
        a list of strings where each item is the corrsponding line in the file.

    Methods
    -------
    `read_in_file()`
    Reads in a file and retruns a list where each line is an item in the list

        Parameters
        ----------
            file_name : str
                a path to an output file
        Returns
        -------
            None
                assignes self.file_list a list of all the lines in a file where each item in the list is an item.
    `set_flag_function()`
    Create the flag_functions dictionary mapping flag strings to the subparsing functions

        Parameters
        ----------
            flag : str
                this is the flag you plan to add to the flag_functions dictionary
            function_string : str
                this is the method you plan to call if the flag is found
        
        Returns
        -------
            None
                Adds to the self.flag_functions dictionary
        
`g16_scraper`
This is a child class of out_file_scraper. To be a general scraper for Gaussian 16 output files

    Attributes
    ----------

    input_line : str
        this is the input line used in the original gjf file

    checkpoint_line : str
        The "%chk=" in the original gjf file

    nproc_line : str
        The "%nproc=" in the original gjf file

    memory_line : str
        The "%mem=" line in the original gjf file

    charge : int
        Represents the charge of the system in the original gjf file

    mult : int
        represents the multiplicity of the system in the original gjf file

    start_geometry: list[str]
        the starting geometry of the sytem in the original gjf file

    Methods
    -------
    `get_input_lines()`
    Extracts the input information of the gaussian file 

        Parameters
        ----------
            self
            index : int
                The index of the line this parsing function's flag is found in the file_list
        Returns
        -------
            None
                assigns respective values to:
                    checkpoint_line : str
                    nproc_line :      str
                    memory_line :     str
                    input_line :      str
                    charge :          int
                    multiplicity :    int
                    start_geometry :  list[str]
    
    `recreate_gjf()`
    Recreates the most basic starting gjf file (does not inclued anything after the starting geometry)

        Parameters
        ----------
            self

        Returns
        -------
            str
                a formatted string of a gjf file from the start of the run

`g16_optfreq`
Child of the g16_scraper. Meant to serve as a file scraper for Gaussian16 frequency calculations

    Attributes
    ----------
    zero_point_correction                          : float
        unit: hartrees/particle
        gives the gaussian calculated floating point number.
    
    thermal_correction_to_energy                   : float
        unit: hartrees/particle
        gives the gaussian calculated floating point number.
    
    thermal_correction_to_enthalpy                 : float
        unit: hartrees/particle
        gives the gaussian calculated floating point number.
    
    thermal_correction_to_gibbs_free_energy        : float
        unit: hartrees/particle
        gives the gaussian calculated floating point number.
    
    sum_of_electronic_and_zero_point_energies      : float
        unit: hartrees/particle
        gives the gaussian calculated floating point number.
    
    sum_of_electronic_and_thermal_enthalpies       : float
        unit: hartrees/particle
        gives the gaussian calculated floating point number.
    
    sum_of_electronic_and_thermal_energies         : float
        unit: hartrees/particle
        gives the gaussian calculated floating point number.

    sum_of_electronic_and_thermal_free_energies    : float
        unit: hartrees/particle
        gives the gaussian calculated floating point number.

    zero_point_energy                              :float
        unit: hartrees/particle
        gives the zero point energy of the system
    
    vibrational_thermal_contributions              : dict {str : tuple(str,float)}
        keys:
            "Thermal_Energy"
                unit : kcal/mol
                returns a list of tuples with the the name : str of the of the contribution at index 0 and the value : float at index 0
            "CV" (specific Heat)
                unit : cal/(mol * kelvin)
                returns a list of tuples with the the name : str of the of the contribution at index 0 and the value : float at index 0
            "S" (Entropy)
                unit : cal/(mol * kelvin)
                returns a list of tuples with the the name : str of the of the contribution at index 0 and the value : float at index 0
        
    Methods
    -------
    `get_thermochemistry_properties()`
    Assigns the thermochemistry properties
        
        Parameters
        ----------
            index : int
                The index of the starting line for the thermochemistry section in an opt freq gaussian job

        Returns
        -------
            None
                Assigns values to the following attributes:
                zero_point_correction                          : float
                thermal_correction_to_energy                   : float
                thermal_correction_to_enthalpy                 : float
                thermal_correction_to_gibbs_free_energy        : float
                sum_of_electronic_and_zero_point_energies      : float
                sum_of_electronic_and_thermal_energies         : float
                sum_of_electronic_and_thermal_enthalpies       : float
                sum_of_electronic_and_thermal_free_energies    : float
                zero_point_energy                              : float
                vibrational_thermal_contributions 



## input_file_maker