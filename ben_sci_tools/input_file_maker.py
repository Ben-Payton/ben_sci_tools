import numpy as np

class xyz_atom:
    """ an atom with x, y, and z coordinates
    """

    def __init__(self,x_val:float,y_val:float,z_val:float,atom_type:str):
        self.x_val = x_val
        self.y_val = y_val
        self.z_val = z_val
        self.atom_type = atom_type

    def as_string(self) -> str:
        """returns a formatted string of atom type and xyz data

        Parameters
        ----------
        None

        Returns
        -------
        A formatted string of atom type and xyz data
        """
        return f"{self.atom_type} {self.x_val} {self.y_val} {self.z_val}"
    
    def as_array(self) -> np.ndarray:
        """returns a numpy array atom type and xyz data

        Parameters
        ----------
        None

        Returns
        -------
        Returns a numpy array for better interadction with cclib
        """
        return np.array([[self.atom_type],
                  [self.x_val,
                   self.y_val,
                   self.z_val]])
    
    def set_xyz(self,xyz_array:np.ndarray[np.float64]):
        """changes xyz coordinates from an array

        Parameters
        ----------
        xyz_array (np.array[float]): an array of xyz coordinates

        Returns
        -------
        Returns a numpy array for better interadction with cclib
        """
        self.x_val = xyz_array[0]
        self.y_val = xyz_array[1]
        self.z_val = xyz_array[2]
    
    @classmethod
    def from_string(cls,line:str):
        line = line.strip(" \n\t")
        line = line.split()
        return cls(line[1],line[2],line[3],line[0])
    
    @classmethod
    def from_xyz_array(cls,atom_type:str,xyz:np.ndarray[np.float64]):
        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        return cls(x,y,z,atom_type)



class xyz_molecule:

    def __init__(self,atom_list:list[xyz_atom]):
        
        self.atom_list = atom_list

    def as_string(self) -> str:
        """returns a formatted string of atom type and xyz data

        Parameters
        ----------
        None

        Returns
        -------
        A formatted string of atom type and xyz data for each atom in the molecule on a new line
        """
        final_string = ""
        for atom in self.atom_list:
            final_string = final_string + atom.as_string() + "\n"

        return final_string[:-1]
    
    def set_xyz(self,xyz_array):
        """sets the xyz coordinates of the molecule to the xyz coordinates of the molecule array

        Parameters
        ----------
        xyz_array a 2D Array where each row is a set of xyz coordinate set for an atom

        Returns
        -------
        None
        """
        for index, coords in enumerate(xyz_array):
            self.atom_list[index].set_xyz(coords)

    
    def add_atom(self,new_atom:xyz_atom):
        """adds an atom to the atom list
        
        Parameters
        ----------
        new_atom (xyz_atom)

        Returns
        -------
        None

        """
        self.atom_list.append(new_atom)


class g16_input:
    """ a base level g16 input file
    """

    def __init__(self, input_line:str, geometry:xyz_molecule, file_name:str,charge:int,spin_mult:int, nproc = 32,mem = 1):
        self.checkpoint = file_name[:-3] + "chk"
        self.file_name = file_name
        self.geometry = geometry
        self.mem = mem
        self.nproc = nproc
        self.input_line = input_line.lower()
        self.extra = ""
        self.title_card = "Title Card"
        self.charge = charge
        self.spin_mult = spin_mult


    def write_file(self):
        """writes a file associated with the g16 input instance
        """
        out_string = f"""%chk={self.checkpoint}
%nproc={self.nproc}
%mem={self.mem}GB
#p {self.input_line}

{self.title_card}

{self.charge} {self.spin_mult}
{self.geometry.as_string()}

{self.extra}


"""
        with open(self.file_name,"w") as file:
            file.write(out_string)

    @classmethod
    def from_file(cls,file_name):
        collect_input = False
        input_line = ""
        nproc = 36
        mem = 1
        charge_collected = False
        charge = 0
        spin_mult = 1
        Title_Card = False
        blank_counter = 0 
        geometry = xyz_molecule([])

        with open(file_name,"r") as file:
            for line in file:
                true_line = line.strip(" \n")

                if "%mem" in true_line:
                    mem = int(true_line.split("=")[1][:-2])

                if "%nproc" in true_line:
                    nproc = int(true_line.split("=")[1])

                if collect_input == True and blank_counter == 0:
                    input_line = input_line + " " + line.strip(" \n")

                if "#p" in true_line:
                    collect_input = True
                    input_line = input_line + line.strip("\n")

                if blank_counter == 2 and charge_collected and true_line != "":
                    geometry.add_atom(xyz_atom.from_string(true_line))

                if blank_counter == 2 and charge_collected == False:
                    true_line = line.strip(" \n\t")
                    charge_mult = true_line.split()
                    charge = charge_mult[0]
                    spin_mult = charge_mult[1]
                    charge_collected = True
                
                if true_line.strip("\t") == "":
                    blank_counter = blank_counter + 1

                                 

        return cls(input_line,geometry,file_name,charge,spin_mult,nproc = nproc,mem = mem)
    

class orca_input:
    '''an object to build orca input files.

    Attributes
    ----------
    
    file_name (str): the name\path of the input file
    
    input_line (str): the input line associated with the orca input file
    
    charge (int): the charge of the system in the orca input file
    
    multiplicity (int): the spin multiplicity of the system in the orca input file
    
    atom_list (list[atom]): a lits of all of the atoms associated with the orca input line
'''

    def __init__(self, geometry : xyz_molecule,file_name ="",input_line = "!", charge = 0,multiplicity = 1) -> None:
        
        self.file_name = file_name
        self.input_line = input_line
        self.charge = charge
        self.multiplicity = multiplicity
        self.geometry = geometry
        pass
    
    def get_atom_list(current_index : int, file_list) -> int:
        ''' helper method to from_file that pulls the atom information from an already existing Orca Input File

        Parameters
        ----------
        
        current_index (int): the current index in a file that already exists

        file_list (list[str]): the orca input file in the format of a list where each line is a str in the list

        Returns
        -------

        atom_list (list[atom]): a list if atom objects from the input file
        current_index (int): the index where the atom list ends
        '''
        line = file_list[current_index]
        # A list for the atoms to be appended to.
        new_geometry = xyz_molecule([])
        # The Last line of the atom list is an astrsk so we continue this loop until we find that
        while "*" not in line:
            # Appending an atom object to the end list based on the current line.
            new_geometry.add_atom(xyz_atom.from_string(line))
            # Itterating to the next line in the list
            current_index = current_index+1
            line = file_list[current_index]
        return  new_geometry , current_index

    @classmethod
    def from_file(cls,file_name:str):
        ''' factory method  to make an orca object from a Orca Input File

        Parameters
        ----------
        
        file_name (str): the name/path to a orca input file

        Returns
        -------

        an orca class object


        '''
        future_input_line = "!"
        # Gives the future file the same name as the inputed one.
        future_file_name = file_name
        # Tells if the charge and multiplicity have been found in the file yet.
        charge_mult_hit = False

        # Opens and formats the file into a list where each line in a string in a list file_list
        with open(file_name) as file:
            file_list = file.readlines()

        current_index = 0
        for index, line in enumerate(file_list):
            if index < current_index:
                continue
            if "xyz" in line:
                # Recognizes the charge, mulitplicity, and xyz atom coordinate section
                current_index = index + 1
                future_charge = line.split()[2]
                future_multiplicity = line.split()[3]
                future_atom_list , current_index = cls.get_atom_list(current_index,file_list)
                charge_mult_hit = True
            if line[0] == "!":
                # recognizes the input lines by a  line starting with '!'
                future_input_line = future_input_line + line.strip("! \n")
            current_index = current_index + 1
        return cls(future_atom_list,file_name=future_file_name , input_line=future_input_line , charge=future_charge , multiplicity=future_multiplicity )
    
    def make_file(self,comment = "") -> None:
        ''' writes the input file

        Parameters
        ----------

        comment (str): an optional comment at the begining of a file

        Returns
        -------

        None

        uses a formatted string to write a file from the orca object
        '''

        # Turns the atom list in to a string.
        atom_list_string = self.geometry.as_string()
        
        file_string = f'''#{comment}
{self.input_line}

%maxcore 16384

%pal
   nprocs 1
end

* xyz {self.charge} {self.multiplicity}
{atom_list_string}
*



'''
        
        with open(self.file_name,"w") as new_file:
            new_file.write(file_string)

