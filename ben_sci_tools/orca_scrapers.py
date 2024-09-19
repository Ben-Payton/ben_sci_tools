###############################################################################
#
# OptFreq class created April 7, 2024 by Isaac Spackman to simplify data
# parsing from ORCA *.out files.
#
# This class inherits from the metaclass OutFile. The hope is that subclasses
# like this one can be defined for general classes of job types (OptFreq, 
# Single Point Energy, TD-DFT, etc.) to extend the functionality of the generic
# OutFile metaclass. These classes should primarily focus on extracting data, 
# rather than data processing, analysis or plotting. These tasks are left to 
# users to implement on a case-by-case project level basis, rather than 
# implementing them here.
#
# The overall vision is to set parsing flags based on whole block sections of the output
# file that call section specific subparsers to extract the data from each 
# section. Each subparser will return a dictionary where each key is a different
# data type available in the current section, and each value is the string, list,
# dict or array containing the data. The current implementation is not absolutely
# true to this vision, but lays thr groundwork for future revisions. More work is 
# needed to establish consistent decorators and interfaces. Rigorous test code is
# also needed. More work is needed to assert values and types for error handling.
#
###############################################################################

import re
import numpy as np

class orca_outfile():
    """
    OutFile is a general class to interpret ORCA output files.
    
    Defines a baseline class applicable to all ORCA log files. Flags and methods 
    defined at this level should be generalized. Require only the path to an 
    ORCA *.out file to initialize this object. File will not be parsed until 
    requested.

    ...

    Attributes (based on whole output block sections)
    ----------
    input: dict
        Dictionary contianing the jobname, command string, charge and multiplicity
        used in the input file.
    xyz : list
        Each element contains xyz coordinates of the optimized geometry
        starting at the top of the file and moving downwards.
    energy : list
        Each element is a float matching the end of the optimization block.
    orbitals : list
        Each element is a tuple (spin up, spin down) where spin up / 
        spin down is an np.array containing the orbital number, occupancy
        and energy. Elements of the spin up / spin down arrays are strings.
    frontier_orbitals : dict
        A summary of the orbital number and energy of the frontier orbitals.

    flag_funcs : dict
        A dictionary where keys are flags appearing in the output file and
        values are string versions of subparsing functions.

        
    Methods
    -------
    set_flag_funcs()
        Defines the string flags used to identify blocks in the output file. 
        Also creates the flag_funcs dictionary.
    
    parse_outfile()
        Open and read the outfile. When a flag is found, pass the line number 
        to the appropriate subparser and return to the file.
    
    get_input()
        Subparser to read the input block. Determines the jobname, commands, 
        charge and multiplicity.
    get_xyz()
        Subparser to read the optimized geometry.
    get_orbitals()
        Subparser to get the orbital population and energy analysis. Also
        gets the frontier orbitals.
    get_mulliken()
        Subparser to get the mulliken population analysis.
    get_loewdin()
        Subparser to get the loewdin population analysis.
    get_mayer()
        Subparser to get the mayer population analysis.
    get_energy()
        Subparser to get the geometry optimized energy.
    get_termination()
        Subparser to get the termination status and overall time.

    """
    
    def __init__(self, filepath : str) -> None:
        '''
        Initialize OutFile object using a filepath.

        Parameters
        ----------
            filepath : str
                The path to an ORCA *.out file.

        Returns
        -------
            None
                Creates an OutFile object.
        '''

        self.path = filepath

        self.set_flag_funcs()

        # -------------------------------------------------------------------------
        # INITIALIZE VARIABLES
        # -------------------------------------------------------------------------

        # OPTIMIZED GEOMETRY
        self.xyz = []
        self.energy = []
        self.orbitals = []
        self.frontier_orbitals = []

        # POPULATION ANALYSIS
        self.mulliken = []
        self.loewdin = []
        self.mayer = []

        # TERMINATION BLOCK
        self.time = None
        self.termination_status = None

    def set_flag_funcs(self):
        '''
        Create the flag_funcs dictionary mapping flag strings to subparsing fucntions.

        Parameters
        ----------
            self

        Returns
        -------
            None
                Creates the self.flag_funcs dictionary.
        '''
        # -------------------------------------------------------------------------
        # DEFINE FLAGS
        # -------------------------------------------------------------------------
        input_flag = "INPUT FILE"
        xyz_flag = "*** FINAL ENERGY EVALUATION AT THE STATIONARY POINT ***"
        orbitals_flag = "ORBITAL ENERGIES"
        mulliken_flag = "MULLIKEN ATOMIC CHARGES AND SPIN POPULATIONS"
        loewdin_flag = "LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS"
        mayer_flag = "* MAYER POPULATION ANALYSIS *"
        energy_flag = "*** OPTIMIZATION RUN DONE ***"
        termination_flag = "****ORCA TERMINATED NORMALLY****"


        # -------------------------------------------------------------------------
        # DEFINE FLAG_FUNCS DICT
        # -------------------------------------------------------------------------
        # functions are written as strings to prevent preemptive execution
        # they will only be evaluated after the line number has been inserted in the 
        # parse_outfile function
        self.flag_funcs = {input_flag : "self.get_input({})", xyz_flag : "self.get_xyz({})", 
                      orbitals_flag : "self.get_orbitals({})", mulliken_flag : "self.get_mulliken({})",
                      loewdin_flag : "self.get_loewdin({})", mayer_flag : "self.get_mayer({})", energy_flag : "self.get_energy({})",
                      termination_flag : "self.get_termination({})"}
    
    def parse_outfile(self):
        '''
        Parse the outfile and generate all data.

        Parameters
        ----------
            self

        Returns
        -------
            None
        '''
        with open(self.path, "r") as f:
            self.lines = f.readlines()
            # skip file header
            self.lines = self.lines[118:] 
            # loop through the file looking for flags
            self.current_index=0
            for index, line in zip(range(0,len(self.lines)), self.lines):
                # skip over sections already read by functions (they update self.current_index)
                if index <= self.current_index:
                    continue
                # figure out which flag it matches and do that function by passing the line number to the function
                # note that the lines are stripped of whitespace for flag matching
                if (flag := line.strip(" \t\n")) in self.flag_funcs.keys():
                    # function will report the current_index back to the class so that this loop skips lines already read
                    eval(self.flag_funcs[flag].format(index))


    def get_input(self, index : int) -> dict:
        '''
        Read the input block and extract the jobname, commands, charge and multiplicity.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            dict
                Dictionary containing the jobname, commands, charge and multiplicity.
        '''

        # configure regex patterns to match
        name_match = r"NAME = /(.*).inp"
        command_match = r"\|.*> !(.*)"
        molecule_specs_match = r"\|.*> \* xyz (\d) (\d)"
        end_match = r"\|.*?\*{4}END OF INPUT\*{4}"

        # loop through the lines storing data when patterns match
        j = index
        section_end = False
        while not section_end:
        
            line = self.lines[(j := j + 1)].strip(" \t\n")
            
            if (jobname := re.search(name_match,line)) != None:
                jobname = jobname.group(0).split("/")[-1]
            if (commands := re.search(command_match,line)) != None:
                commands = commands.group(1)
            if (molecule_specs := re.search(molecule_specs_match, line)) != None:
                charge, multiplicity = molecule_specs.groups()
                charge = int(self.charge)
                multiplicity = int(self.multiplicity)

            section_end = re.search(end_match, line) != None

        self.input = {"jobname" : jobname, "commands" : commands, "charge" : charge, "multiplicity" : multiplicity}

        # report the current index at the end of the section back to the class
        self.current_index = j

        return self.input

    def get_xyz(self, index : int) -> list:
        '''
        Determine the optimized xyz cartesian geometry.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            list
                Each item in the list is a complete xyz geometry matching the flag
                and pattern requirements. There may be multiple matches.
        '''

        # configure regex patterns to match
        end_match = "-{28}"

        # loop through the lines storing data when patterns match
        j = index + 5
        section_end = False
        xyz_coords = []
        while not section_end:
        
            line = self.lines[(j := j + 1)].strip(" \t\n")
            xyz_coords.append(line)

            section_end = re.search(end_match,line) != None

        self.xyz.append("\n".join(xyz_coords[:-2]))

        # report the current index at the end of the section back to the class
        self.current_index = j

        return self.xyz

    def get_orbitals(self, index : int) -> list:
        '''
        Parse the orbital occupation and energy.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            list
                Each item in the list is a tuple (spin up, spin down). Spin up/down are np.arrays 
                containing the orbital number, occupancy and energy in (Eh) and (eV).
                There may be multiple matches and multiple tuples in the list.
        '''

        # configure patterns to match
        orbital_match = r"(\d+) +(-?\d+\.\d+) +(-?\d+\.\d+) +(-?\d+\.\d+)"
        end_match = "\*{32}"

        # loop through the lines storing data when patterns match
        j = index + 3
        section_end = False
        orbital_list = []
        while not section_end:
        
            line = self.lines[(j := j + 1)].strip(" \t\n")
            
            if (orbital_data := re.search(orbital_match, line)) != None:

                orbital_list.append(np.array(orbital_data.groups()))

            section_end = re.search(end_match,line) != None

        # split the matched data into spin up and spin down groups
        updown_split = int(len(orbital_list) / 2 - 1)
        spin_up = np.array(orbital_list[:updown_split], dtype=float)
        spin_down = np.array(orbital_list[updown_split:], dtype=float)

        # analyze the orbital data for frontier energies
        self.get_frontier_orbitals((spin_up, spin_down))

        self.orbitals.append((spin_up, spin_down))

        # report the current index at the end of the section back to the class
        self.current_index = j

        return self.orbitals

    def get_frontier_orbitals(self, orbital_data : tuple) -> dict:
        '''
        Parse the orbital occupation and energy. 

        !NOTE!
        Function requires edits to work on open shell species also. 

        Parameters
        ----------
            orbital_data : tuple
                A tuple of np.arrays containing (spin up, spin down) data.

        Returns
        -------
            dict
                A dictionary containing the frontier orbital numbers and energies in (Eh).
        '''

        for spin_data in orbital_data:
            # if the system is closed shell
            if self.multiplicity == 1:
                # find the first index where the occupancy goes from 1 -> 0 and extract the data
                LUMO_index = np.where(spin_data[:, 1] == 0)[0][0]
                HOMO_index = LUMO_index - 1

                LUMO_energy_Eh = spin_data[LUMO_index, 2]
                HOMO_energy_Eh = spin_data[HOMO_index, 2]

                self.frontier_orbitals.append({"HOMO_number" : HOMO_index, "LUMO_number" : LUMO_index, 
                                                   "HOMO_energy(Eh)" : HOMO_energy_Eh, "LUMO_energy(Eh)" : LUMO_energy_Eh})
                
                # only need to look at spin up to determine HOMO/LUMO in closed shell, so skip spin down
                break

            # this is where we neeed edits for open shell
            else:
                raise LookupError("DOES NOT WORK ON OPEN SHELL")

        return self.frontier_orbitals
    
    def get_mulliken(self, index : int) -> list:
        '''
        Read the mulliken population analysis table for spin and partial charges.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            list
                Each item in the list is a np.array of strings. Each np.array contains
                the element name, partial charge and spin population for the whole system.
        '''

        # configure regex patterns to match
        mulliken_match = r"\d+ +([a-zA-Z]+) : +(-?\d+\.\d+) +(-?\d+\.\d+)"
        end_match = "Sum of atomic charges .*"

        # loop through the lines storing data when patterns match
        j = index + 1
        section_end = False
        mulliken_list = []
        while not section_end:
        
            line = self.lines[(j := j + 1)].strip(" \t\n")
            
            if (mulliken_data := re.search(mulliken_match, line)) != None:
                
                mulliken_list.append(np.array(mulliken_data.groups()))

            section_end = re.search(end_match,line) != None

        self.mulliken.append(np.array(mulliken_list))

        # report the current index at the end of the section back to the class
        self.current_index = j

        return self.mulliken

    def get_loewdin(self, index : int) -> list:
        '''
        Read the loewdin population analysis table for spin and partial charges.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            list
                Each item in the list is a np.array of strings. Each np.array contains
                the element name, partial charge and spin population for the whole system.
        '''

        # configure regex patterns to match
        loewdin_match = r"\d+ +([a-zA-Z]+) : +(-?\d+\.\d+) +(-?\d+\.\d+)"
        end_match = "-{52}"

        # loop through the lines storing data when patterns match
        j = index + 1
        section_end = False
        loewdin_list = []
        while not section_end:
        
            line = self.lines[(j := j + 1)].strip(" \t\n")
            
            if (loewdin_data := re.search(loewdin_match, line)) != None:

                loewdin_list.append(np.array(loewdin_data.groups()))

            section_end = re.search(end_match,line) != None

        self.loewdin.append(np.array(loewdin_list))

        # report the current index at the end of the section back to the class
        self.current_index = j

        return self.loewdin
    
    def get_mayer(self, index :int) -> list:
        '''
        Read the mayer population analysis table for spin and partial charges.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            list
                Each item in the list is a np.array of strings. Each np.array contains
                the element name, partial charge and spin population for the whole system.
                !NOTE!
                Need to review the mayer table to make identify all 6 items from the table.
        '''
        
        # configure regew patterns to match
        mayer_match = r"\d+ +([a-zA-Z]+) +(-?\d+\.\d+) +(-?\d+\.\d+) +(-?\d+\.\d+) +(-?\d+\.\d+) +(-?\d+\.\d+) +(-?\d+\.\d+)"
        end_match = "-{7}"

        # loop through the lines storing data when patterns match
        j = index + 10
        section_end = False
        mayer_list = []
        while not section_end:
        
            line = self.lines[(j := j + 1)].strip(" \t\n")
            
            if (mayer_data := re.search(mayer_match, line)) != None:

                mayer_list.append(np.array(mayer_data.groups()))

            section_end = re.search(end_match,line) != None

        self.mayer.append(np.array(mayer_list))

        # report the current index at the end of the section back to the class
        self.current_index = j

        return self.mayer

    def get_energy(self, index : int) -> list:
        '''
        Get the final energy from the geometry optimization.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            list
                Each item in the list is a float corresponding to a final energy value.
                There may be multiple matches to the flag, resulting in multiple values
                in the list.
        '''

        energy = float(self.lines[index-3].strip(" \t\n").split()[-1])
        self.energy.append(energy)

        self.current_index = index

        return self.energy
        
    def get_termination(self, index : int) -> dict:
        '''
        Parse the data from the file termination block.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            dict
                Helpful info like the termination status and total runtime.
                !NOTE!
                Need to make termination status flag more robust, currently won't be called unless job terminated normally.
        '''

        self.termination_status = "Normal"
        self.time = self.lines[index + 1].strip("\n")

        self.termination = {"termination_status" : self.termination_status, "time" : self.time}

        return self.termination



class orca_optfreq(orca_outfile):
    """
    OptFreq is a inherits from the general class OutFile to interpret ORCA 
    output files from OptFreq calculations.
    
    Defines a subclass specific to OptFreq ORCA log files. Flags and methods 
    defined at this level are specific to all OptFreq calculations. Require 
    only the path to an ORCA *.out file to initialize this object. 
    File will not be parsed until requested.

    ...

    Attributes (based on whole output block sections)
    ----------
    freqs: list
        List of np.arrays containing frequency data. 
        !NOTE!
        Need to review file to identify types of each element in the array.
    symmetry : list
        Each element is a string correponding to the point group identified.
        If the point groups are identified incorrectly, the entropic/enthalpic
        corrections may be untrustworthy.

        
    Methods
    -------
    set_new_flag_funcs()
        Defines the string flags used to identify blocks in the output file. 
        Also creates the flag_funcs dictionary.
    
    get_freqs()
        Subparser to read the IR frequency table. Determines the force constants and intensities.
    get_symmetry()
        Subparser to extract the interpreted symmetry.
  
    """
    def __init__(self, filepath):
        '''
        Initialize OptFreq object using a filepath.

        Parameters
        ----------
            filepath : str
                The path to an ORCA *.out file.

        Returns
        -------
            None
                Creates an OptFreq object.
        '''

        # -------------------------------------------------------------------------
        # INITIALIZE VARIABLES
        # -------------------------------------------------------------------------
        self.freqs = []
        self.symmetry = []

        # -------------------------------------------------------------------------
        # INITIALIZE OutFile OBJECT
        # -------------------------------------------------------------------------
        orca_outfile.__init__(self, filepath)

        # -------------------------------------------------------------------------
        # EXTEND FLAG_FUNCS WITH CASE-SPECIFIC FLAGS
        # -------------------------------------------------------------------------
        self.set_new_flag_funcs()
       

    def set_new_flag_funcs(self):
        '''
        Update the inherited flag_funcs dictionary mapping flag strings to subparsing fucntions.

        Parameters
        ----------
            self

        Returns
        -------
            None
                Creates the self.flag_funcs dictionary.
        '''
        # -------------------------------------------------------------------------
        # DEFINE FLAGS
        # -------------------------------------------------------------------------
        IR_flag = "IR SPECTRUM"
        symmetry_flag = "ENTHALPY"
        
        # -------------------------------------------------------------------------
        # UPDATE FLAG_FUNCS DICT
        # -------------------------------------------------------------------------
        self.new_flag_funcs = {IR_flag: "self.get_freqs({})", symmetry_flag : "self.get_symmetry({})"}
        self.flag_funcs.update(self.new_flag_funcs)
        
    def get_freqs(self, index : int) -> list:
        '''
        Read the IR block and extract the frequencies and intensities.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            list
                Each element in the list is an np.array containing the IR data.
                !NOTE! 
                Need complete definition of each row/ column in the np.array added to docs
        '''
        
        # configure regex patterns to match
        freq_match = r"(\d+): +(-?\d+\.\d+) +(-?\d+\.\d+) +(-?\d+\.\d+) +(-?\d+\.\d+) +\(( ?-?\d+\.\d+) +(-?\d+\.\d+) +(-?\d+\.\d+)\)"
        end_match = "-{26}"

        # loop through the lines storing data when patterns match
        j = index + 5
        section_end = False
        freq_list = []
        while not section_end:
        
            line = self.lines[(j := j + 1)].strip(" \t\n")
            
            if (freq_data := re.search(freq_match, line)) != None:
               
                freq_list.append(np.array(freq_data.groups()))

            section_end = re.search(end_match,line) != None

        self.freqs.append(np.array(freq_list))

        # report the current index at the end of the section back to the class
        self.current_index = j

        return self.freqs

    def get_symmetry(self, index : int) -> list:
        '''
        Read the symmetry block and extract the point group.

        Parameters
        ----------
            index : int
                Starting line number to begin search. Note line numbers shifted by 
                118 due to skipped header.

        Returns
        -------
            list
                Each element in the list is string. There may be multiple matches to the flag
                resulting in variable length lists.
        '''

        # configure regex patterns to match
        symmetry_match = r"Point Group: +(.*),.*"
        end_match = "-{7}"

        # loop through the lines storing data when patterns match
        j = index + 12
        section_end = False
        while not section_end:
        
            line = self.lines[(j := j + 1)].strip(" \t\n")
            
            if (symmetry_data := re.search(symmetry_match, line)) != None:
                
                self.symmetry.append(symmetry_data.group(1))

            section_end = re.search(end_match,line) != None

        # report the current index at the end of the section back to the class
        self.current_index = j

        return self.symmetry