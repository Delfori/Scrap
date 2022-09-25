import pandas as pd
import numpy as np
import os


folder = r'C:\Users\sergknut\Documents\Parse_Shafa\df_test'
folder = os.getcwd()
files = os.listdir(folder)
files.sort()
df = pd.DataFrame()

def create_new_df(file):
    dat, username = file[:8], file[9:-4]
    df_new = pd.read_csv(file, delimiter='|')
    df_new['File'] = file
    df_new['User'] = username
    df_new['Date'] = dat
    df_new['Current Price'] = df_new['Current Price'].astype('str')
    df_new['Current Price'] = df_new['Current Price'].str.extract(r'(\d+)').astype('float')
    df_new['Old Price'] = df_new['Old Price'].astype('str')
    df_new['Old Price'] = df_new['Old Price'].str.extract(r'(\d+)').astype('float')
    df_new['Date'] = pd.to_datetime(df_new['Date'], format='%d%m%Y')
    return df_new

def compare_dfs(df1, df2):
    comp = df1[['Link', 'User']].merge(df2[['Link', 'User']],indicator = True, how='left', left_on='Link', right_on='Link').loc[lambda x : x['_merge']=='left_only']
    rez_df = df1[df1['Link'].isin(comp['Link'])]
    return rez_df

for file in files:
    if file[-4:] != '.csv' or file[:4] == 'sales':
        continue
    df_new = create_new_df(file)
    print(f'Append {file}')
    df = pd.concat((df, df_new))

dfs = dict(tuple(df.groupby('Date')))
dates = list(dfs.keys())
sales = pd.DataFrame()
new_items =  pd.DataFrame()

for i, dat in enumerate(dates):
    if i == 0:
        continue
    df1 = dfs[dates[i-1]]
    df2 = dfs[dates[i]]

    filt = np.intersect1d(df1.User.unique(), df2.User.unique())
    
    sales = pd.concat((sales,compare_dfs(df1,df2)))
    sales = sales[sales.User.isin(filt)]
    new_items = pd.concat((new_items,compare_dfs(df2,df1)))
    new_items = new_items[new_items.User.isin(filt)]
    
sales['Flow'] = 'Sales'
new_items['Flow'] = 'New Items'
sales.Date += pd.Timedelta(days=1)
report = pd.concat((sales, new_items))

#sales.to_json('sales.json', orient='records')
sales.to_csv('sales.txt', sep='\t', index=False)
new_items.to_csv('new_items.txt', sep='\t', index=False)
report.to_csv('report.txt', sep='\t', index=False)