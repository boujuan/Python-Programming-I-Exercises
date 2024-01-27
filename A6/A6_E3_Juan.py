import pandas as pd
import numpy as np

# Read previously defined csv file with Error-Log column
df = pd.read_csv('series_df2.csv', delimiter=';')
# Replace NaN values in 'Error-Log' column with '0kay'
df['Error-Log'] = df['Error-Log'].fillna('0kay')
print(df, '\n')

# Group by 'Error-Log' and calculate mean of 'Data 1' and 'Data 2'
grouped_df = df.groupby('Error-Log')[['Data 1', 'Data 2']].mean()
print(grouped_df, '\n')

# Set the index to the square product of the current index
df.index = df.index ** 2

# Replace the rows in 'Data 1' and 'Data 2' that have 'Error' in 'Error-Log' with np.nan
df.loc[df['Error-Log'] == 'Error', ['Data 1', 'Data 2']] = np.nan
print(df)