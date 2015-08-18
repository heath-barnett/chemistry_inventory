__author__ = 'heath'
import sys, os, csv, jinja2
import pandas as pd
import numpy as np

data = pd.read_csv('data/lab_schedule.csv', header=0)
# collig = [line for line in csv.DictReader(open('collig_data.csv'))]
desk = pd.read_csv('data/All_Rooms.csv',names=['Room','Desk','ID','Combo'],header=0)
desk['Combo'] = desk['Combo'].str.replace('\'','')

# report = pd.pivot_table(data, index=['Class','Instructor','Lab'],values=['Section','PreLab','Shift'])
report = data.groupby(['Class', 'Lab'])
for x in report:
    print(x)

Chem1003A=[3,18,33,48,63,78,91,108,123,138,153,168]
Chem1003B=[9,24,39,54,69,84,99,114,129,144,159,174]
Chem1009A=[5,17,35,47,65,77,95,107,125,137,155,167]
Chem1009B=[8,20,38,50,68,80,98,110,128,140,158,170]
Chem1009C=[11,23,41,53,71,83,101,113,131,143,161,173]
# orphans ?? 15,30,45,60,75,90,105,120,135,150,165,180
Chem1010A=[1,10,19,28,32,40,49,58,61,70,79,88,91,100,109,118,121,130,139,148,151,160,169,178]
Chem1010B=[2,7,16,25,34,43,52,59,62,67,76,85,94,103,112,119,124,133,142,149,154,163,172,179]
Chem1010C=[4,13,22,29,32,37,46,55,64,73,82,89,92,97,106,115,122,127,136,145,152,157,166,175]
Chem2031A=[1101,1102,1103,1104,1105,1106,1107,1108,1109,1110,1111,1112,1113,1114,1115,1116,1117,1118,1119,1120,1121,1122,1123,1124]
Chem2031B=[1301,1302,1303,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,1315,1316,1317,1318,1319,1320,1321,1322,1323,1324]
Chem2031C=[1501,1502,1503,1504,1505,1506,1507,1508,1509,1510,1511,1512,1513,1514,1515,1516,1517,1518,1519,1520,1521,1522,1523,1524]
Chem2031D=[1701,1702,1703,1704,1705,1706,1707,1708,1709,1710,1711,1712,1713,1714,1715,1716,1717,1718,1719,1720,1721,1722,1723,1724]
Chem2033A=[3101,3102,3103,3104,3105,3106,3107,3108,3109,3110,3111,3112,3113,3114,3115,3116,3117,3118,3119,3120,3121,3122,3123,3124]
Chem2033B=[3301,3302,3303,3304,3305,3306,3307,3308,3309,3310,3311,3312,3313,3314,3315,3316,3317,3318,3319,3320,3321,3322,3323,3324]
Chem2033C=[3501,3502,3503,3504,3505,3506,3507,3508,3509,3510,3511,3512,3513,3514,3515,3516,3517,3518,3519,3520,3521,3522,3523,3524]
Chem2033D=[1801,1802,1803,1804,1805,1806,1807,1808,1809,1810,1811,1812,1813,1814,1815,1816,1817,1818,1819,1820,1821,1822,1823,1824]
# Change the default delimiters used by Jinja such that it won't pick up
# brackets attached to LaTeX macros.
report_renderer = jinja2.Environment(
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%{',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath('.'))
)

class_list = [Chem1009A,Chem1009B,Chem1009C,Chem1003A,Chem1003B,Chem1010A,Chem1010B,Chem2031A,Chem2031B,Chem2031C,Chem2033A,Chem2033B,Chem2033C]
room_list = np.int16([230, 232, 233, 235,240,242])
# for j in y:
#     for i in x:
#         out = desk[desk['Desk'].isin(i) & (desk['Room'] == np.int16(j))]
#         outsort=out.sort_index(by='Desk',ascending=True)
#
# outsort = outsort[['Desk','ID','Combo']].to_latex(index=False)

# for i, row in data.iterrows():
#     if row['Desk'] == 'Chem1009A':
#         template = report_renderer.get_template('templates/report_template_1009A.tex')
#     else:
#         template = report_renderer.get_template('templates/report_template.tex')
for i, row in data.iterrows():
    template = report_renderer.get_template('templates/report_template.tex')
    cid = row['Class']
    section = row['Section']
    instructor = row['Instructor']
    lab = row['Lab']
    dlc = desk[desk['Desk'].isin([row['Desk']]) & (desk['Room'] == np.int16(lab))]
    dlc_sort = dlc.sort_index(by='Desk',ascending=True)
    print(dlc)
    dlc_sort = dlc_sort.to_latex(index=False)

    # filename = str(cid) + '_' + str(section) + '_Desk_Combinations.tex'
    # folder = 'latex'
    # outpath = os.path.join(folder,filename)
    # outfile = open(outpath,'w')
    # outfile.write(template.render(cid = cid, section = section, lab = lab, instructor = instructor, dlc = dlc_sort))
    # outfile.close()
    # os.system("pdflatex -output-directory=" + folder + " " + outpath)
