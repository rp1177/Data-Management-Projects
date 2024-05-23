import csv

#For context, originally developed this data manipulation project in a jupyter notebook, but had to convert/transfer it into a py file. 
def main():

    #Part 1:  Find out what percentage of "fire" type pokemons are at or above the "level" 40. (This is percentage over fire pokemons only, not all pokemons)
    #extract all fire-types:
    firetypes_lvl = []
    total_firetypes = []
    with open('pokemonTrain.csv') as pokemonfile:  
        reader = csv.reader(pokemonfile) 
        next(reader)
    
        for index,row in enumerate(reader):
            if row[4] == 'fire':
                total_firetypes.append(row)
                if float(row[2]) >= 40.0:
                    firetypes_lvl.append(row)

#after extracting the total fire types involved in the file and ones greater or eq.
#to level 40, calculate the percentage and write to the file.

    final_result = ( len(firetypes_lvl) / len(total_firetypes) ) * 100
    final_result = int(round(final_result))

    pokemon1 = open('pokemon1.txt', 'w')
    pokemon1.write("Percentage of fire type Pokemons at or above level 40: " + str(final_result))
    pokemon1.close()

###################################################################################################################################
    #Part 2:  Fill in the missing "type" column values (given by NaN) by mapping them from the corresponding "weakness" values. You will see that typically a given pokemon weakness has a fixed "type", but there are some exceptions. So, fill in the "type" column with the most common "type" corresponding to the pokemon’s "weakness" value.

    common_weakness = {} #make a mapping of weakness-type frequency
    #key -> weakness . Value -> List of types weak to that type.

    data = []

#open the original csv file to get a frequency of common weaknesses based on type. Populate common_weakness dictionary.
    with open('pokemonTrain.csv') as pokemonfile:  
        reader = csv.reader(pokemonfile) 
        next(reader)
    
        for index,col in enumerate(reader):
            data.append(col)
        
            if col[4] != 'NaN':
            #if key is not in the dictionary, make the key happen as well as list val.
                if col[5] in common_weakness:
                    common_weakness[col[5]].append(col[4])
                else:
                    common_weakness[col[5]] = [col[4]]

        common_weakness = {key: sorted(value) for key, value in common_weakness.items()} #make sure the values are in alphabetical order.
        print(common_weakness)
    
    
#Populate the dictionary with the entire csv traversal. 

# Process the data
    for col in data:
        if col[4] == 'NaN':
            for key, value in common_weakness.items():
                if col[5] == key:
                    max_freq = max(set(value), key=value.count)
                    col[4] = max_freq  # Replace 'NaN' with max_freq

# Write the modified data back to the CSV file
    with open('pokemonTrain.csv', 'w', newline='') as final_pokemon_file:
    
        writer = csv.writer(final_pokemon_file)
        header = ['id', 'name', 'level','personality','type','weakness','atk','def', 'hp', 'stage']
        writer.writerow(header)
        writer.writerows(data)

###################################################################################################################################
    #Part 3: Fill in the missing (NaN) values in the Attack ("atk"), Defense ("def") and Hit Points ("hp") columns as follows:

    #a.) Set the pokemon level threshold to 40.
    #b.) For a Pokemon having level above the threshold (i.e. > 40), fill in the missing value for atk/def/hp with the average values of atk/def/hp of Pokemons with level > 40. So, for instance, you would substitute the missing "atk" value for Magmar (level 44), with the average "atk" value for Pokemons with level > 40. Round the average to one decimal place.
    #c.) For a Pokemon having level equal to or below the threshold (i.e. <= 40), fill in the missing value for atk/def/hp with the average values of atk/def/hp of Pokemons with level <= 40. Round the average to one decimal place.

# solve part b and c by getting the averages, by doing so we will rely on lists to compute these averages.
    atk_grt_40 = []
    atk_less_40 = []

    def_grt_40 = []
    def_less_40 = []

    hp_grt_40 = []
    hp_less_40 = []

    data = []

    with open('pokemonTrain.csv', 'r') as pokemonfile:
        reader = csv.reader(pokemonfile)
        next(reader)
    
        for index,col in enumerate(reader):
            #target col6 -> atk:
            data.append(col)
        
            if col[6] != 'NaN' and float(col[2]) > 40.0:
                atk_grt_40.append(float(col[6]))
            
            if col[6] != 'NaN' and float(col[2]) <= 40.0:
                atk_less_40.append(float(col[6]))
            
            if col[7] != 'NaN' and float(col[2]) > 40.0:
                def_grt_40.append(float(col[7]))
        
            if col[7] != 'NaN' and float(col[2]) <= 40.0:
                def_less_40.append(float(col[7]))
            
            if col[8] != 'NaN' and float(col[2]) > 40.0:
                hp_grt_40.append(float(col[8]))
        
            if col[8] != 'NaN' and float(col[2]) <= 40.0:
                hp_less_40.append(float(col[8]))

#Calculate the averages for atk, def, hp depending on level being either less than or eq 40 or greater. 
    average_atk_grt_40 = round((sum(atk_grt_40) / len(atk_grt_40)),1)
    average_atk_less_40 = round((sum(atk_less_40) / len(atk_less_40)),1)

    avg_def_grt_40 = round((sum(def_grt_40) / len(def_grt_40)), 1)
    avg_def_less_40 = round((sum(def_less_40) / len(def_less_40)),1)

    avg_hp_grt_40 = round((sum(hp_grt_40) / len(hp_grt_40)), 1)
    avg_hp_less_40 = round((sum(hp_less_40) / len(hp_less_40)), 1)

    print(average_atk_grt_40)
    print(average_atk_less_40)
    print("_____________________")
    print(avg_def_grt_40)
    print(avg_def_less_40)
    print("_____________________")
    print(avg_hp_grt_40)
    print(avg_hp_less_40) 
    
#Now that we have the rounded averages, lets add this into pokemonTrain:

# Process the data
    for col in data:
        if col[6] == 'NaN' and float(col[2]) > 40.0:
            col[6] = average_atk_grt_40
        if col[6] == 'NaN' and float(col[2]) <= 40.0:
            col[6] = average_atk_less_40
    
        if col[7] == 'NaN' and float(col[2]) > 40.0:
            col[7] = avg_def_grt_40
    
        if col[7] == 'NaN' and float(col[2]) <= 40.0:
            col[7] = avg_def_less_40
        
        if col[8] == 'NaN' and float(col[2]) > 40.0:
            col[8] = avg_hp_grt_40
    
        if col[8] == 'NaN' and float(col[2]) <= 40.0:
            col[8] = avg_hp_less_40
        
        
    # Write the modified data back to the CSV file
    with open('pokemonTrain.csv', 'w', newline='') as final_pokemon_file:
    
        writer = csv.writer(final_pokemon_file)
        header = ['id', 'name', 'level','personality','type','weakness','atk','def', 'hp', 'stage']
        writer.writerow(header)
        writer.writerows(data)

# ____________________________________________________________________________________________________________________
#Make a new CSV Copy file called "pokemonResult.csv" and this is where modifications will happen for tasks 2 and 3:
#This copy will have no NaN values involved.

    with open('pokemonTrain.csv', 'r') as original_file, open('pokemonResult.csv', 'w', newline='') as copy_file:
        reader = csv.reader(original_file)
        writer = csv.writer(copy_file)
    
        for row in reader:
            writer.writerow(row)
# ____________________________________________________________________________________________________________________
    
###################################################################################################################################
    #Part 4: Create a dictionary that maps pokemon types to their personalities. This dictionary would map a string to a list of strings. For example: {"fire": ["docile", "modest", ...], "normal": ["mild", "relaxed", ...], ...} Your dictionary should have the keys ordered alphabetically, and also items ordered alphabetically in the values list, as shown in the example above.

#Use the pokemonResult.csv to do this, open it first.

    type_to_personality = {} #empty dictionary to populate

    with open('pokemonResult.csv', 'r') as pokemonfile:
        reader = csv.reader(pokemonfile)
        next(reader)
    
        for index,col in enumerate(reader):
            if col[4] in type_to_personality: #if the key is in the dictionary, append the value as it currently exists.
                type_to_personality[col[4]].append(col[3])
            else:
                type_to_personality[col[4]] = [col[3]]

    #After constructing dictionary, sort it alphabetically, including its inner string list:
        type_to_personality = {key: sorted(value) for key, value in type_to_personality.items()} #sorting the inner items first alphabetically
    
        sort_keys = sorted(type_to_personality.keys()) #sort the keys then
        type_to_personality = {key: type_to_personality[key] for key in sort_keys}
    
        print(type_to_personality)
    

#Now we write this dictionary out to a new file as follows:
    pokemon4 = open('pokemon4.txt', 'w')
    pokemon4.write('Pokemon type to personality mapping:\n\n')


    for key,value in type_to_personality.items():
        pokemon4.write('\t'+key + ': ' + str(value).split('[')[1].split(']')[0].replace("'", '') + '\n')
    
    pokemon4.close()

###################################################################################################################################
    #Part 5: Find out the average Hit Points ("hp") for pokemons of stage 3.0. Your program should print the value as follows (replace ... with value):

    #Average hit point for Pokemons of stage 3.0 = ... You should round off the value, like in #1 above.
    #Print the value to a file named "pokemon5.txt" If you do not print to a file, or your output file name is not exactly as required, you will get 0 points.

    #extract all stage 3.0:

    stage_3_with_hp = []



    with open('pokemonResult.csv') as pokemonfile:  
        reader = csv.reader(pokemonfile) 
        next(reader)
    
        for index,col in enumerate(reader):
            if col[9] == '3.0': #check if stage is 3.0, if so append the hp value it corresponds to in the list.
                stage_3_with_hp.append(float(col[8]))
        
        if len(stage_3_with_hp) != 0:
            final_result = round((sum(stage_3_with_hp) / len(stage_3_with_hp)))

    pokemon5 = open('pokemon5.txt', 'w')
    pokemon5.write("Average hit point for Pokemons of stage 3.0 = " + str(final_result))
    pokemon5.close()

if __name__ == "__main__":
    main()