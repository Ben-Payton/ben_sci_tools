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
    `read_in_file`
    Reads in a file and retruns a list where each line is an item in the list

        Parameters
        ----------
            file_name : str
                a path to an output file
        Returns
        -------
            None
                assignes self.file_list a list of all the lines in a file where each item in the list is an item.
        '''

## input_file_maker