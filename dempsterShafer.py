## THIS IS WHERE YOUR DEMPSTER SHAFER CODE (AND THE GRAD STUDENT PRE-PROVIDED CODE) SHOULD GO 

# THIS CODE DOES NOT REQUIRE EDITING, BUT SHOULD BE PUT INTO YOUR dempsterShafer.py module
# Your graduate teammate wrote this code. It shouldn't need any changes.
# Dempster Shafer combination, belief, and plausibility calculations.

class dempsterShafer:

    def __init__(self):
        return

    @staticmethod    
    def get_belief(mass):
        """
        Purpose: For a given set of masses, get the belief - 
        the lower bound of probability, such that it is the sum of all
        masses where B is a subset of A
        
        keyword arguements:
        
        mass -- the mass for the weights you would like to get DS 
        style belief for
        
        return: the belief for DS
        """
        beliefs = []
        
        for i in range(0, len(mass)):
            subset_calc = [k[1] for k in mass if set(k[0]).issubset(set(mass[i][0]))]
            belief = round(sum(subset_calc),4)
            beliefs.append([mass[i][0], belief])
            
        return beliefs

    @staticmethod
    def get_plausibility(mass):
        """
        Purpose: For a given set of masses, get the belief - 
        the lower bound of probability, such that it is the sum of all
        masses where B is a subset of A
        
        keyword arguements:
        
        mass -- the mass for the weights you would like to get DS 
        style plausibility for
        
        return: the belief for DS
        """
        plausibilities = []
        
        for i in range(0, len(mass)):
            subset_calc = [k[1] for k in mass if set(k[0]).intersection(set(mass[i][0]))]
            plausibility = round(sum(subset_calc),4)
            plausibilities.append([mass[i][0], plausibility])
            
        return plausibilities

    @staticmethod
    def check_sums(detections):
            """
            Purpose: Confirm that the masses within the text file sum to 1. 
            
            keyword arguments: 
            detections -- loaded detection nested list of the following format
            [[['a'], 0.5],[['b'], 0.3], [['a','b'], 0.2]]
            
            return:
            validate -- return whether or not this detection list is valad (aka the masses sum to 1)
            """
            
            return sum([i[1] for i in detections])

    @staticmethod
    def combine_masses(d1, d2):
        """
        Purpose: Combine loaded, validated masses in accordance with the rules of dempster-shafer
        
        keyword arguments:
        d1 -- detection from first sensor considered of the format
        [[['a'], 0.5],[['b'], 0.3], [['a','b'], 0.2]]
        d2 -- detection from second sensor considered of the format
        [[['a'], 0.5],[['b'], 0.3], [['a','b'], 0.2]]
        
        return:
        if valid mass file, return loaded detections in the following format
        [[['a'], 0.5], [['b'], 0.3], [['a','b'], 0.2]]
        
        if not valid mass file, return error
        """
        
        combined_masses = []
        
        # Combine by multiplication and generate all subgroup components, including the
        # Null-space created by this fusion
        for hypothesis_d1 in d1:
            for hypothesis_d2 in d2:
                joint_list = list(set(hypothesis_d1[0]).intersection(hypothesis_d2[0]))
                if len(joint_list) == 0:
                    joint_list = ['null']
                        
                if joint_list in [x[0] for x in combined_masses]:
                    for i in combined_masses:
                        if i[0] == joint_list:
                            i[1] += round(hypothesis_d1[1] * hypothesis_d2[1],4)


                else:
                    combined_masses.append([joint_list, round(hypothesis_d1[1] * hypothesis_d2[1],4)])

        ##Scale by null accordingly if it exists/has been created during fusion
        if ['null'] in [i[0] for i in combined_masses]:
            K = 1 - round([i[1] for i in combined_masses if i[0] == ['null']][0],4)
        else: 
            K = 1
        combined_masses = [[i[0],round(i[1]/K,6)] for i in combined_masses if i[0] != ['null']]
        
        if round(dempsterShafer.check_sums(combined_masses),2) == 1:
            
            return combined_masses

        else:
            print(str(round(dempsterShafer.check_sums(combined_masses),4)))
            return """an error has occurred, mass fusion has not returned a result of 1. 
                    For dempster-shafer to run, it must hold that masses sum to 1. Your
                    mass fusion has returned: """+ str(round(dempsterShafer.check_sums(combined_masses),4))