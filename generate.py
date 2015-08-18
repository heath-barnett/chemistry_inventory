__author__ = 'heath'
import sys, os, csv, jinja2
import pandas as pd
import numpy as np

data = pd.read_csv('data/lab_schedule.csv', header=0)
# collig = [line for line in csv.DictReader(open('collig_data.csv'))]

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

template = report_renderer.get_template('templates/report_template.tex')

for i, row in data.iterrows():
    cid = row['Class']
    section = row['Section']
    instructor = row['Instructor']
    lab = row['Lab']
    filename='output_' + str(i) + '.tex'
    folder='latex'
    outpath=os.path.join(folder,filename)
    outfile=open(outpath,'w')
    outfile.write(template.render(cid = cid, section=section,lab=lab,instructor=instructor))
    outfile.close()
    os.system("pdflatex -output-directory=" + folder + " " + outpath)
