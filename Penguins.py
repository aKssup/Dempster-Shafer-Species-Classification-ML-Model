# We can run this file to get results!

# Imports:
from pandas import DataFrame
from Dataset import Dataset
from dempsterShafer import dempsterShafer
import matplotlib.pyplot as plt
import seaborn as sns

# Inheriting properties from Dataset parent class
class Penguins(Dataset):

    # Constructor
    def __init__(self, fileName: str):
        super().__init__(fileName)

    # Initializes the num argument for the head() call
    def get_data(self, numb: int):

        # Initializing the numb value (which controls how many rows are shown)
        # and the pandaObj, which is the panda object holding our csv file data
        if numb < 0:
            raise ValueError("numb argument is negative")
        if numb == 0:
            return self.pandaObj.head()
        else: 
            return self.pandaObj.head(numb)

    # Gets the combined visualization for data
    def get_graphs(self):

        # Let's Get a sense of what the data looks like:
        # Creating 2x2 matrix-like visual of 4 subplots total
        fd, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Iterating and plotting values to create an histogram for each column
        # Ex: culmen_length_mm is for the 0,0 index in the 2x2 matrix
        for fd, ax in [('culmen_length_mm',axes[0,0]), ('culmen_depth_mm',axes[0,1]), ('flipper_length_mm',axes[1,0]), ('body_mass_g',axes[1,1])]:

            # Specifying step plot and showing which axis to use (ax)
            sns.histplot(self.pandaObj, x=fd, hue='species', element='step', ax=ax)

        # Creating a seaborn joint plot. kde represents the kernel density
        sns.jointplot(

            # Setting data to our panda object (has the csv), same logic seen above
            data = self.pandaObj,
            x = "culmen_length_mm", y="culmen_depth_mm", hue="species",
            kind = "kde"
        )

    # The method that runs our analysis and gets a prediction
    def prediction(self, type: str):

        # Holds an array with all the unique species names
        uniqueSpecies = self.pandaObj[type].unique()

        # Array with all the fields, manually defined
        fields = ['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g']

        # Assigns the classRangeOutput array to classRange
        classRange = self.classRangeOutput("species", fields)

        # Defining data variables
        correct = 0
        incorrect = 0
        indeterminate = 0

        # Iterating through each penguin, which a row in our dataset
        for index, row in self.pandaObj.iterrows():
            
            # Dictionary to hold our masses 
            masses = {}

            # Iterating through each attribute
            for f in fields:
                hypothesisCount = self.powerset(uniqueSpecies)
                h = self.hypothesis(uniqueSpecies, classRange, f, row[f])
                self.hypothesisCounts(hypothesisCount, h, uniqueSpecies)
                masses[f] = hypothesisCount
                    
            # Doing the mass combinations. The reason we do them individually in pairs of 2 is to
            # simplify the process and retain our relative weights.
            masses_comb1 = dempsterShafer.combine_masses(masses['culmen_length_mm'], masses['culmen_depth_mm'])
            masses_comb2 = dempsterShafer.combine_masses(masses_comb1, masses['flipper_length_mm'])
            masses_comb3 = dempsterShafer.combine_masses(masses_comb2, masses['body_mass_g'])

            # Find the highest output of combined Mass
            vals = 0
            for i in range(0, len(masses_comb3)):
                if masses_comb3[i][1] > vals:
                    most_likely = masses_comb3[i][0]
                    vals = masses_comb3[i][1]
            if len(most_likely) == 1:
                if most_likely[0] == row["species"]:
                    correct += 1
                else:
                    incorrect += 1

            ## For situations where multiple classes are selected as the most likely
            ## We declare them wrong. 
    
            ## What could we do here to provide a second way of differentiating between the two classes? 
            ## Try something.
            elif len(most_likely) == 2:

                # Gets the DSV attribute
                attr = self.fsv_classifier(fields, most_likely)
                di = {}

                # Adds values to the dictionary above in terms of the di values. di = {a - mean(a)}
                for i in range(len(most_likely)):
                    val = abs(row[attr] - self.get_AVG_forType(most_likely[i], attr))
                    di[most_likely[i]] = val
                
                # Checking if the prediction is correct or incorrect
                if min(di, key = di.get) == row["species"]:
                    correct += 1
                else:
                    incorrect += 1
            else:
                indeterminate += 1

            # For each observation; we should also be able to get a sense of our belief and the plausibility.
            Penguins.get_output(masses_comb3) 
        
        print("We had ", correct, "correct classifications") 
        print("We had ", incorrect, "incorrect classifications")
        print("We had ", indeterminate, "indeterminate classifications")
        print(f"We had an {correct/(correct+incorrect+indeterminate)*100}% accuracy")
    
    # Calling the get_output() function returns a Dataframe with the hypothesis, assigned mass weight, belief, and plausibility
    @staticmethod
    def get_output(mass):
        
        # Calling belief and plausibility using our mass array (masses_comb3)
        belief = dempsterShafer.get_belief(mass)
        plausibility = dempsterShafer.get_plausibility(mass)

        # Makes an array by our 4 values in question
        together = [[mass[i][0], mass[i][1], belief[i][1], plausibility[i][1]] for i in range(0, len(mass))]
        return DataFrame(together, columns = ['hypothesis', 'mass', 'belief', 'plausibility'])

    # The function outputs the attribute that should be used for DRC in an indeterminate case
    def fsv_classifier(self, arr, speciesList: list):

        # Creating a dictionary to hold all species' data values
        classRange = {}

        # Iterating through each unique species 
        for c in speciesList:

            # Creating another dictionary to store sd for the 4 types of attributes per species
            fieldSd = {}
            for f in arr:

                # Each attribute has its own sd (standard deviation)
                fieldSd[f] = self.get_Sd_forSpecies(c, f)

            # At the end class range holds species with respective attribute and their sds
            classRange[c] = fieldSd

        # Creating a dictionary for sds of each column (regardless of species type)
        totalSds = {}

        # Iterating through each attribute and finding the sd
        for f in arr:
            totalSds[f] = self.get_Sd_forColAndSpecies(f, speciesList)

        # Creating the final fsv dictionary that holds FSV's for each attribute
        fsv = {}

        # Iterating through each attribute
        for f in arr:
            attrTotal = 1
            
            # Iterating through speciesList 
            for c in speciesList:

                # Multiplying attrTotal with the sd for a given species (for a given field)
                attrTotal *= classRange[c][f]
                
            # Adding each attribute's FSV to the fsv dictionary
            fsv[f] = attrTotal / totalSds[f]

        # Returning the attribute with the lowest FSV
        return min(fsv, key = fsv.get) # culmen_depth_mm

    @staticmethod
    def main():

        # Creating penguins object:
        penguins = Penguins("penguins.csv")

        # Getting the first 5 data values
        print(penguins.get_data(0))

        # Calling the graph function and showing illustrations
        penguins.get_graphs()
        plt.show()
        penguins.prediction("species")

# Runs our "main" method
Penguins.main()