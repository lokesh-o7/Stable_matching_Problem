"""
Pseudo code:
read the data
Assign numbers to the preference for both male and female based on the input.

While all male are matched:
    choose female from preference list of male in the most prefered order
    if the female is not matched -> match with male
    if female is already matched ->
        check the preference of the current male and already matched male according the female prefrence list
        if the new male is more prefered change the match. 
            Remove the already matched male from matching list and find new match for him
        Otherwise match the male with the next most preferred female.
"""
import sys
n=len(sys.argv)
if n>2:
    raise ValueError("More than 1 file/command provided. Only specify the filepath in following manner \n python assignment1.py Tests/input.txt")

#taking input from the text file
filename = sys.argv[1]
file = open(filename,"r+")
n = file.readline() # reading the first line to get the number of male/female
n = int(n)
# creating a dictonary for male and female. Where key is name of person and values are the lsit prefrences
male = {}
female = {}
count = 0
for line in file:
    if count<n:
        male[line.split()[0]] = line.split()[1:]
    else:
        female[line.split()[0]] = line.split()[1:]
    count+=1
file.close()

# A function to give the prefrence number for every value in the value list for the corresponding keys.
#example for {'Albert' : ['Diane', 'Emily', 'Fergie']} output will be {'Albert': {'Diane':0, 'Emily':1, 'Fergie':2}}
def pref_to_rank(pref):
    return {
        person: {partner: index for index, partner in enumerate(person_pref)}
        for person, person_pref in pref.items()
    }
matching={} #final result will be appended into this dictionary

male_name = list(male.keys()) #list of all males
female_name = list(female.keys()) #list of all females

rank_male = pref_to_rank(male) #creating the preference list for every male
rank_female = pref_to_rank(female) #creating the preference list for every female

#using the concept of set to add/delete the male once they have been matched. 
# After being matched a male is added to the set, if a better potential match is found then the 
# other male is added to the set and male from the existing match will be added back to the list
unmatched_male = set(male_name) 
while len(unmatched_male)>0:
    current_male  = unmatched_male.pop() #checking the match one by one for each male and female from the given list
    current_female = male[current_male].pop(0)
    if current_female not in matching: #If there is no current match for the female, they will be matched with the male
        matching[current_female]=current_male
    #If there is a match for the female, the prefrence is compared betweeen existing partner and current male.
    #If current male is more preffered over the existing partner, they are replaced
    else: 
        existing_partner = matching[current_female]
        if rank_female[current_female][existing_partner] > rank_female[current_female][current_male]:
            matching[current_female] = current_male
            unmatched_male.add(existing_partner)
        else:
            unmatched_male.add(current_male)

#writing the result into the output file
if "input" in filename:
    output_filename = filename.replace("input","output")
else:
    output_filename = filename.replace('.txt','Output.txt')
output_file = open(output_filename,'w')
#Since the requied output is "male female" converting the final dictionary into the required format.
for key,value in matching.items():
    output_file.write("{} {}\n".format(value,key))
output_file.close()
        