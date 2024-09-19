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
    
`rxn_coord_list_format`
rxn_coord_list_format takes a list of energies or enthalpies and returns a new list where each value is duplicated. This formatted list can be used to create a step-like reaction coordinate plot.

    Parameters
    ----------
    reaction_list (list[float]) :  a list of floating point numbers representing energies or enthalpies

    Returns
    -------
    a list of floating point numbers with each value duplicated for better plotting of reaction coordinates

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

### Functions

### Classes

`xyz_atom`
an atom with x, y, and z coordinates

    Attributes
    ----------
    x_val : float
        x postion
    y_val : float
        y postion
    z_val : float
        z postion
    atom_type : str
        the atomic coded for an atom i.e. C for carbon

    Methods
    -------

    `as_string()`
    returns a formatted string of atom type and xyz data

        Parameters
        ----------
        None

        Returns
        -------
        A formatted string of atom type and xyz data

`xyz_molecule`
a list of xyz_atoms

    Attributes
    ----------
        atom_list : list[xyz_atom]

    Methods
    -------
    
    `as_string()`
    returns a formatted string of atom type and xyz data

        Parameters
        ----------
        None

        Returns
        -------
        A formatted string of atom type and xyz data for each atom in the molecule on a new line
        """
    
    `add_atom()`
    adds an atom to the atom list
        
        Parameters
        ----------
        new_atom (xyz_atom)

        Returns
        -------
        None

`g16_input`
A formatting object for g16_inputs

    Attributes
    ----------

    checkpoint : str
        The name of the checkpoint file
    file_name : str
        The name of the associated input file
    geometry : xyz_molecule
        The systems geometry information 
    mem : int
        The memory usage of the calculation in GB. default is 1
    nproc : int
        the number of processors used in the cacluation the default is 36
    input_line : str
        The input line of the input file
    extra : str
        Any information that may come after the geometry section
    title_card : str
        The Title card of the input file
    charge : charge
        The charge of the system
    spin_mult : int
        The spin multiplicity of the system

## colors
colors contains color pallets. in the form of a dictionary where keys are the name of the color and values are hex representations.

`mines_primary`

"dark_blue":"#21314d",
"blaster_blue" : "#09396C",
"light_blue" :  "#879EC3" ,
"colorado_red" : "#CC4628",
"pale_blue" : "#CFDCE9"

`mines_neutral`

"white" : "#FFFFFF",
"light_gray" : "#AEB3B8",
"silver" : "#81848A",
"dark_gray" : "#75757D"

`mines_accecnt`

"earth_blue" : "#0272DE",
"muted_blue" : "#57A2BD",
"energy_yellow" : "#F0F600",
"golden_tech" : "#F1B91A",
"environment_green" : "#80C342",
"red_flannel" : "#B42024"