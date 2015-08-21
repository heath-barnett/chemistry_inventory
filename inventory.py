__author__ = 'heath'
import os, jinja2
import pandas as pd
import numpy as np

stock = pd.read_csv('data/inv_stock.csv',encoding='utf-8',header=0)
master = pd.read_csv('data/inv_lab.csv',encoding='utf-8',header=0)
# TODO  Incorpate Desk and Locker assignments
master['Required'] = master['Required'].astype(float)
master.rename(columns={'Notes':'Preperation'},inplace=True)
inv = stock[['Name','Stock','Containers','Location','Notes']]

pd.set_option('display.max_columns',8)
pd.set_option('display.max_rows',200)

result = pd.merge(master, inv, how='left',on='Name',suffixes=(' 1', ' 2'))
df=result.groupby(['Lab','Experiment'])
fout = open('all_labs_req.txt','w')
for name, group in df:
    fout.write(str(name[0]))
    fout.write('\n')
    fout.write(group.to_string())
    fout.write('\n')
fout.close()

def labmat(df):
    for (section, exp), group in df:
        print('Chemistry', section, '- Laboratory', exp)
        print(group[['Name', 'Required', 'Unit']].to_string(index=False))
        print('\n')


def status(dX):
    if (dX['Stock'] - dX['Required']*13) / dX['Required'] > 1.2:
        return 'No'
    else:
        return 'Re-Order'


invCompare = result[['Name', 'Lab', 'Unit', 'Required', 'Stock', 'Type']]
compare = pd.DataFrame({'Name': invCompare['Name'], 'Status': invCompare['Stock'] >= invCompare['Required'],'Projection': invCompare['Stock']-invCompare['Required']})
invCompare = pd.merge(invCompare,compare,how='left')
gnoes = pd.DataFrame({'Name': invCompare['Name'], 'Type': invCompare['Type'], 'Stock': invCompare['Stock'], 'Required': invCompare['Required'],
                      'Status': invCompare.apply(status, axis=1)})

reagents=gnoes[(gnoes.Status == 'Re-Order') & (gnoes.Type == 'Reagent')].to_string(index=False)


consumables=gnoes[(gnoes.Status == 'Re-Order') & (gnoes.Type == 'Consumable')].to_string(index=False)

# df=master.groupby(['Lab','Experiment'])
# for (section,exp), group in df:
#         print('Chemistry', section,'- Laboratory',exp)
#         print(group[['Name','Required','Unit']].to_string(index=False))
#         print('\n')

desk = pd.read_csv('data/All_Rooms.csv',names=['Room','Desk','ID','Combo'],header=0)
desk['Combo'] = desk['Combo'].str.replace('\'','')
schedule = pd.read_csv('data/lab_schedule.csv', header=0)

grp_sched = schedule.groupby('Class')
f= open("reagents.txt",'w')
f.write('Reagents \n')
f.write(reagents)
f.close()

f= open("consumables.txt",'w')
f.write('Consumables \n')
f.write(consumables)
f.close()

fout = open('all_labs_requirements.txt','w')

for (cls, sec), group in df:
    fout.write('Chemistry '+ str(cls) + ' - Experiment '+  str(sec) + '\n')
    fout.write(group[['Name','Required','Unit']].to_string(index=False)+ '\n')
    fout.write('\n')
fout.close()