__author__ = 'heath'
import sys, os, csv, jinja2
import pandas as pd
import numpy as np

data = pd.read_csv('data/lab_schedule_spring_2016.csv', header=0)
# collig = [line for line in csv.DictReader(open('collig_data.csv'))]
desk = pd.read_csv('data/All_Rooms.csv',names=['Room','Desk','ID','Combo'],header=0)
desk['Combo'] = desk['Combo'].str.replace('\'','')

faculty={'Instructor':['Heath Barnett','Buddy Barnett','Sharon Cruse','Emad El-Giar','Sahar Atwa','Andrew Cox','Richard Thurlkill','Gary Findley','Brandy Courtney'],
   'Email':['hbarnett@ulm.edu','bbarnett@ulm.edu','cruse@ulm.edu', 'elgiar@ulm.edu','atwa@ulm.edu','cox@ulm.edu','thurlkill@ulm.edu','g.l.findley@ulm.edu','courtney@ulm.edu'],
   'Office':['204','206','201','200','227','205','203','202','224']}

df_faculty = pd.DataFrame(faculty)

Chem141 = []
Chem1003A=[3,18,33,48,63,78,91,108,123,138,153,168]
Chem1003B=[9,24,39,54,69,84,99,114,129,144,159,174]
Chem1009A=[5,17,35,47,65,77,95,107,125,137,155,167]
Chem1009B=[8,20,38,50,68,80,98,110,128,140,158,170]
Chem1009C=[11,23,41,53,71,83,101,113,131,143,161,173]
Chem1009Z = [4,22,32,46,64,82,92,106,122,136,152,166]
Chem1009X=[3,18,33,48,63,78,91,108,123,138,153,168]
# orphans ?? 15,30,45,60,75,90,105,120,135,150,165,180
Chem1010A=[1,10,19,28,32,40,49,58,61,70,79,88,91,100,109,118,121,130,139,148,151,160,169,178]
Chem1010B=[2,7,16,25,34,43,52,59,62,67,76,85,94,103,112,119,124,133,142,149,154,163,172,179]
Chem1010C=[4,13,22,29,32,37,46,55,64,73,82,89,92,97,106,115,122,127,136,145,152,157,166,175]
# organic codes have to have room number in the ID due to format in which the desk numbers were arranged
Chem2031A240=[1101,1102,1103,1104,1105,1106,1107,1108,1109,1110,1111,1112,1113,1114,1115,1116,1117,1118,1119,1120,1121,1122,1123,1124]
Chem2031B240=[1301,1302,1303,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,1315,1316,1317,1318,1319,1320,1321,1322,1323,1324]
Chem2031C240=[1501,1502,1503,1504,1505,1506,1507,1508,1509,1510,1511,1512,1513,1514,1515,1516,1517,1518,1519,1520,1521,1522,1523,1524]
Chem2031A242=[1201,1202,1203,1204,1205,1206,1207,1208,1209,1210,1211,1212,1213,1214,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224]
Chem2031B242=[1401,1402,1403,1404,1405,1406,1407,1408,1409,1410,1411,1412,1413,1414,1415,1416,1417,1418,1419,1420,1421,1422,1423,1424]
Chem2031C242=[1601,1602,1603,1604,1605,1606,1607,1608,1609,1610,1611,1612,1613,1614,1615,1616,1617,1618,1619,1620,1621,1622,1623,1624]
Chem2033A240=[3101,3102,3103,3104,3105,3106,3107,3108,3109,3110,3111,3112,3113,3114,3115,3116,3117,3118,3119,3120,3121,3122,3123,3124]
Chem2033A242=[3201,3202,3203,3204,3205,3206,3207,3208,3209,3210,3211,3212,3213,3214,3215,3216,3217,3218,3219,3220,3221,3222,3223,3224]
Chem2033B240=[3301,3302,3303,3304,3305,3306,3307,3308,3309,3310,3311,3312,3313,3314,3315,3316,3317,3318,3319,3320,3321,3322,3323,3324]
Chem2033B242=[3401,3402,3403,3404,3405,3406,3407,3408,3409,3410,3411,3412,3413,3414,3415,3416,3417,3418,3419,3420,3421,3422,3423,3424]
Chem2033C240=[3501,3502,3503,3504,3505,3506,3507,3508,3509,3510,3511,3512,3513,3514,3515,3516,3517,3518,3519,3520,3521,3522,3523,3524]
Chem2033C242=[3601,3602,3603,3604,3605,3606,3607,3608,3609,3610,3611,3612,3613,3614,3615,3616,3617,3618,3619,3620,3621,3622,3623,3624]
Chem2033D240=[1701,1702,1703,1704,1705,1706,1707,1708,1709,1710,1711,1712,1713,1714,1715,1716,1717,1718,1719,1720,1721,1722,1723,1724]
Chem2033D242=[1801,1802,1803,1804,1805,1806,1807,1808,1809,1810,1811,1812,1813,1814,1815,1816,1817,1818,1819,1820,1821,1822,1823,1824]

# Change the default delimiters used by Jinja such that it won't pick up brackets attached to LaTeX macros.
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

for i, row in data.iterrows():
    template = report_renderer.get_template('templates/report_template.tex')
    cid = row['Class']
    section = row['Section']
    instructor = row['Instructor']
    prelab = row['PreLab']
    lab = row['Lab']
    schedule = row['Schedule']
    time = row['Time']
    semester = row['Semester']
    dlc_id = row['Desk']
    dlc = desk[(desk['Desk'].isin(eval(dlc_id))) & ((desk['Room'] == np.int16(lab)))]
    dlc_sort = dlc.sort_index(by='Desk',ascending=True)
    dlc_sort = dlc_sort[['Desk', 'ID', 'Combo']]
    dlc_sort = dlc_sort.to_latex(index=False)
    filename = str(cid) + '_' + str(section) + '_' + str(instructor).replace(' ','_') + '_Desk_Combinations.tex'
    folder = 'latex/spring16'
    outpath = os.path.join(folder, filename)
    outfile = open(outpath, 'w')
    outfile.write(template.render(cid=cid, section=section, prelab=prelab, lab=lab, instructor=instructor,time=time, schedule=schedule, semester=semester,dlc_sort=dlc_sort))
    outfile.close()
    os.system("pdflatex -output-directory=" + folder + " " + outpath)
