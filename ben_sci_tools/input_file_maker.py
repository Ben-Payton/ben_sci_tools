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
    
    @classmethod
    def from_string(cls,line:str):
        line = line.strip(" \n\t")
        line = line.split()
        return cls(line[1],line[2],line[3],line[0])
    
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