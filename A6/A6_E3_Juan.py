############################################ JULIA E1 PART ############################################
import numpy as np
import pandas as pd

#########################################E1.a#########################################
random_array = np.random.randint(0, 20, size=(2, 24)) #array shape: (2, 24)
#print(random_array)

#########################################E1.b#########################################
# directly from the array
df_direct = pd.DataFrame(random_array.T, columns=['Data1', 'Data2']) #T. for transpose 

#dict from np.array 
random_dict = {}
for index, row in enumerate(random_array):
    random_dict[f"Data {index + 1}"] = row
df_dict = pd.DataFrame(random_dict)


# from two pd.Series objects created from the individual array columns
serie1_df = pd.Series(random_array[1,:])
serie2_df = pd.Series(random_array[0,:])

series_combined  = pd.DataFrame() #empty data frame 
# Now we can add the columns one-by-one:
series_combined["Data 1"] = serie1_df
series_combined["Data 2"] = serie2_df

print(f"E1.b1\n:{df_direct}") #E1.b1
print()
print(f"E1.b2\n:{df_dict}")  #E1.b2
print()
print(f"E1.b3\n:{series_combined}") #E1.b3
#########################################E1.c#########################################

series_combined["DataProd"] = series_combined["Data 1"]*series_combined["Data 2"]
print("E1.c")
print(series_combined)
############################################ JULIA E2 PART ############################################
#########################################E2.a#########################################
series_combined = series_combined.astype(np.float64)
#print(series_combined.dtypes) #print data type for whole dataframe

#########################################E2.b#########################################
series_combined.to_csv('series_df.csv', index=False, float_format='%.2f') #index= True or False to include / exclude the index column 

#########################################E2.d#########################################
df = pd.read_csv('series_df.csv', delimiter=';')

# Print the DataFrame
print(df)

#what happened with the blank rows? 
print()
print(f"Data type of Error-cell: {type(df['Error-Log'][2])}") 
print(f"Data type of blank cell: {type(df['Error-Log'][0])}")  
print(f"Data type new column: {type(df['Error-Log'])}")
########################################################################################

############################################ JUAN E3 PART ############################################
# Replace all nan values in Error-Log column by 0kay:
# Use group functionality to group data into 0kay and Error and
# calculate the mean values of both Data-columns when grouped
# Set the index in df to the square product of the current index
# Replace the rows in the Data1, Data2 columns thet have an Error
# entry in the Error-Log column by np.nan (use only 1 line)
########################################################################################

