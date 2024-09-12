import glob


def statp(file_pattern:str) -> str:
    '''takes a file patern and returns the number of stationary points in each file that fits that pattern.

    Parameters
    ----------
    file_patern (str) :  a string that matches a certain string

    Returns
    -------
    a string that gives nomber of occurences and line numbers of stationary points

'''
    # String that will be returned later
    results_string = ""
    #Loop through each file name that matches the pattern
    for name in glob.glob(file_pattern):
        indexes = []
        count = 0
        with open(name,'r') as file:
            file_lines = file.readlines()
        #Loop through the lines of the file
        for index, line in enumerate(file_lines):
            #Add line numbers if stationary point is present
            if "-- Stationary point found." == line.strip("\n\t "):
                count = count + 1
                indexes.append(index)
        # Add results to results string
        results_string = results_string + f"{name+":":<35}{count}\n{indexes}\n"
    return results_string