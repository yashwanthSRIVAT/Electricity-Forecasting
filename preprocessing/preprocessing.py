import pandas as pd
import numpy as np

# create an empty dataframe with columns named 'day1' to 'day8'
new = pd.DataFrame(columns=['day' + str(i) for i in range(1, 9)])

# read the shanghai data, remove date column, convert to numpy array and flatten that array
arr = pd.read_csv('../media/Shanghai_data.csv').iloc[:, 1:].to_numpy().flatten()

# add rows to the dataframe
i, j = 0, 8
while( j != 7000):
    new = new.append(pd.Series(arr[i:j], index=new.columns), ignore_index=True)
    i += 1
    j += 1

# create a new file to store the updated dataset
new.to_csv('../media/Processed_Data.csv', index=False)