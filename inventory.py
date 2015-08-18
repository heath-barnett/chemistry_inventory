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


def labmat(df):
    for (section, exp), group in df:
        print('Chemistry', section, '- Laboratory', exp)
        print(group[['Name', 'Required', 'Unit']].to_string(index=False))
        print('\n')


print(labmat(df))
def status(dX):
    if (dX['Stock'] - dX['Required']) / dX['Required'] > 1.2:
        return 'No'
    else:
        return 'Re-Order'


invCompare = result[['Name', 'Lab', 'Unit', 'Required', 'Stock', 'Type']]

compare = pd.DataFrame({'Name': invCompare['Name'], 'Status': invCompare['Stock'] >= invCompare['Required'],'Projection': invCompare['Stock']-invCompare['Required']*4})

invCompare = pd.merge(invCompare,compare,how='left')
dd = invCompare

gnoes = pd.DataFrame({'Name': invCompare['Name'], 'Type': dd['Type'], 'Stock': dd['Stock'], 'Required': dd['Required'],
                      'Status': dd.apply(status, axis=1)})

print(gnoes[(gnoes.Status == 'Re-Order') & (gnoes.Type == 'Reagent')].to_string())


#print(invCompare[['Name','Lab','Unit','Required','Stock','Status','Projection']].to_string())


# df=master.groupby(['Lab','Experiment'])
# for (section,exp), group in df:
#         print('Chemistry', section,'- Laboratory',exp)
#         print(group[['Name','Required','Unit']].to_string(index=False))
#         print('\n')

desk = pd.read_csv('data/All_Rooms.csv',names=['Room','Desk','ID','Combo'],header=0)
desk['Combo'] = desk['Combo'].str.replace('\'','')
schedule = pd.read_csv('data/lab_schedule.csv', header=0)
#print(master)

Chem1003A=[3,18,33,48,63,78,91,108,123,138,153,168]
Chem1003B=[9,24,39,54,69,84,99,114,129,144,159,174]
Chem1009A=[5,17,35,47,65,77,95,107,125,137,155,167]
Chem1009B=[8,20,38,50,68,80,98,110,128,140,158,170]
Chem1009C=[11,23,41,53,71,83,101,113,131,143,161,173]
# orphans ?? 15,30,45,60,75,90,105,120,135,150,165,180
Chem1010A=[1,10,19,28,32,40,49,58,61,70,79,88,91,100,109,118,121,130,139,148,151,160,169,178]
Chem1010B=[2,7,16,25,34,43,52,59,62,67,76,85,94,103,112,119,124,133,142,149,154,163,172,179]
Chem1010C=[4,13,22,29,32,37,46,55,64,73,82,89,92,97,106,115,122,127,136,145,152,157,166,175]
print(desk[desk['Desk'].isin(Chem1003A) & (desk['Room'] == 232)])
grp_sched = schedule.groupby('Class')
for group in grp_sched:
    print(group)
