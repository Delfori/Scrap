import csv
import numpy as np
import pandas as pd

file = r'C:\Users\sergknut\Documents\Parse_Shafa\test\11082022_solar_sp.csv'
file2 = r'C:\Users\sergknut\Documents\Parse_Shafa\test\11082022_solar_sp_transf.txt'

lst = [str(i) for i in range(10)]
print('*****'*30)

with open(file, encoding='utf-8', mode='r') as f:
    contents = f.readlines()

    result = []
    temp_str = ''
    #print(contents)
    arr_to_transform = contents[:0:-1]
    for i, line in enumerate(arr_to_transform):
        # print(i, line)
        if arr_to_transform[i][0] in lst:
            result.append(arr_to_transform[i] + temp_str)
            temp_str = ''
        else:
            temp_str = arr_to_transform[i] + temp_str
    
    result = [contents[0]] + result[::-1]



# with open(file2, encoding='utf-8', mode='w') as f:
#     write = csv.writer(f)
#     write.writerows(result)

np.savetxt(file2, 
           result,
           fmt ='% s',
           encoding='utf-8')

