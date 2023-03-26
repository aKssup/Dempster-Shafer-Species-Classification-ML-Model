# Imports
import pandas as pd

class Dataset:

    # Constructor 
    def __init__(self, fileName: str):

        # If the file name is blank or null, an error is raised
        if len(fileName) < 1 or fileName == None:
            raise ValueError("fileName argument is empty or null")

        # Initializing attributes of the class
        self.fileName = fileName

        # The drop pandas call removes all rows (because axis = 0) that have less than 6 non-NA values
        self.pandaObj = pd.read_csv(fileName).dropna(axis = 0, thresh = 6)

    # Getter for pandaObj
    def get_pandaObj(self):
        return self.pandaObj

    # Returns a dictionary with types (ex: Adelie species) and their sub attributes (ex: culmen_length_mm)
    # The type parameter is the column that is desired (ex: species)
    # The list arr parameter is a list of desired attributes (culmen_length_mm ... body_mass_g)
    def classRangeOutput(self, type, arr: list):
        classRange = {}

        # Iterates through each unique type(species) --> Adelie, Chinstrap, Gentoo
        for c in self.pandaObj[type].unique():
            fieldRange = {}

            # For each species, it assigns a dictionary that has key (attribute) and value (value of attribute)
            for f in arr:
                fieldRange[f] = (self.pandaObj[self.pandaObj[type] == c][f].min(), self.pandaObj[self.pandaObj[type] == c][f].max())
            classRange[c] = fieldRange

        # At the end we are returning a dictionary for each species with sub dictionaries for respective attributes (and their values)
        return classRange

    # Gives us the power set for a given set s (ex: s represents the unique species in our dataset)
    # The power set includes the set itself (array with all species) and the null set (empty array)
    # In essence, the power set is the combination of all subsets for a given set
    def powerset(self, s):
        output = []
        x = len(s)

        # Iterating for the number of 2^x possibilities using bitwise operators 
        for i in range(1 << x):

            # If the i-th bit is 1, then the given val should be included
            val = [s[j] for j in range(x) if (i & (1 << j))]

            # Each subset is initialized with a 0 weight/value
            initial = [val, 0.0]
            output.append(initial)

        # Returns an array with each index representing an array. The sub array's 0 index is the subset
        # combination while the 1 index is the 0.0 weight/value
        return output
    
    # Assigning value to one hypothesis by comparing it to the classRange for a given attribute (if it falls between min and max)
    def hypothesis(self, uniqueSpecies, classRange, fieldName, value):
        hset = []

        # Iterating through uniqueSpecies and adding values to hset are in range(min, max)
        for c in uniqueSpecies:
            if (classRange[c][fieldName][0] <= value and value < classRange[c][fieldName][1]): 
                hset.append(c)
        return hset

    # Assigning a weight to the hypothesis depending on whether the hypothesis contains 1, 2, or all 3 classes
    def hypothesisCounts(self, hypothesisCount, h, uniqueSpecies):
        
        # If our hypothesis set contains all unique elements, then it is automatically weighted 1
        if len(h) > 0 and len(h) < len(uniqueSpecies):
            for i in range(0, len(hypothesisCount)):
                if(hypothesisCount[i][0] == h):
                    hypothesisCount[i][1] += 0.9
                    hypothesisCount[-1][1] += 0.1
        else:
            hypothesisCount[-1][1] += 1

    # Gets the standard deviation for an attribute column, given one species
    def get_Sd_forSpecies(self, speciesName, attribute):
        rows = self.pandaObj['species'] == speciesName
        col = self.pandaObj.loc[rows, attribute]
        return col.std()
    
    # Gets the standard deviation for an attribute column, given multiple species
    def get_Sd_forColAndSpecies(self, attribute, speciesList):
        rows = self.pandaObj['species'].isin(speciesList)
        col = self.pandaObj.loc[rows, attribute]
        return col.std()

    # Gets the mean for an attribute column, given one species
    def get_AVG_forType(self, speciesName, attribute):
        rows = self.pandaObj['species'] == speciesName
        col = self.pandaObj.loc[rows, attribute]
        return col.mean()