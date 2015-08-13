__author__ = 'heath'
import pandas as pd
import numpy as np

stock = pd.read_csv('data/inv_stock.csv',encoding='utf-8',header=0)
master = pd.read_csv('data/inv_lab.csv',encoding='utf-8',header=0)
# TODO  Incorpate Desk and Locker assignments
master['Required'] = master['Required'].astype(float)
master.rename(columns={'Notes':'Preperation'},inplace=True)
inv = stock[['Name','Stock','Containers','Location','Notes']]

pd.set_option('display.max_columns',0)
pd.set_option('display.max_rows',200)

result = pd.merge(master, inv, how='left',on='Name',suffixes=(' 1', ' 2'))
df=result.groupby(['Lab','Experiment'])


def status(dX):
    if (dX['Stock'] - dX['Required']) / dX['Required'] > 1.2:
        return 'No'
    else:
        return 'Re-Order'
invCompare = result[['Name','Lab','Unit','Required','Stock']]
compare = pd.DataFrame({'Name': invCompare['Name'], 'Status': invCompare['Stock'] >= invCompare['Required'],'Projection': invCompare['Stock']-invCompare['Required']*4})

invCompare = pd.merge(invCompare,compare,how='left')
dd = invCompare
gnoes = pd.DataFrame(
    {'Name': invCompare['Name'], 'Stock': dd['Stock'], 'Required': dd['Required'], 'Pojection': dd['Projection'] <= 0,
     'Remaining': dd['Stock'] - dd['Required'], 'Status': dd.apply(status, axis=1)})
print(gnoes.to_string())
#print(invCompare[['Name','Lab','Unit','Required','Stock','Status','Projection']].to_string())


# df=master.groupby(['Lab','Experiment'])
# for (section,exp), group in df:
#         print('Chemistry', section,'- Laboratory',exp)
#         print(group[['Name','Required','Unit']].to_string(index=False))
#         print('\n')