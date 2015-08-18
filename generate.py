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

# output = open('latex/output_pdf3.tex', 'w')
# output.write(template.render(data = data,collig=collig))
# output.close()
# os.system("pdflatex -output-directory=" + folder + " " + outpath)
# os.system('xelatex.exe -synctex=1 -interaction=nonstopmode latex/output_pdf3.tex')
