# -*- coding: utf-8 -*-

'''Create the necessary support files from the input Excel files
for the program operation.

    stand.pkl, skel.pkl,

from proposals(Excel files):
    p1, p2, p3.pkl etc. for each proposal


from master.xlsx:
    master.pkl,
    fur.pkl,
    sg.pkl,
    last_month.pkl,
    active_each_month.pkl

from pay_tables:
    pay_table_with_rsv_with_fur.pkl,
    pay_table_no_rsv_with_fur.pkl,
    idx_pay_table_with_rsv_with_fur.pkl,
    idx_pay_table_no_rsv_with_fur.pkl

created by editor tool:
     ds_edit.pkl,
     slider_vals.pkl,
     squeeze_vals.pkl,
     new_order.pkl

example usage in jupyter notebook:
    %run build_files.py master_sample
'''

import pandas as pd
import numpy as np

import functions as f
import config as cf

# MASTER FILE:
if cf.sample_mode:
    sample_prefix = cf.sample_prefix
    master = pd.read_excel('sample_data/' + sample_prefix + 'master.xlsx')
else:
    master = pd.read_excel('excel/master.xlsx')

master.set_index('empkey', drop=False, inplace=True)
master.to_pickle('dill/master.pkl')

# FUR
fur = master[['fur']]
fur.to_pickle('dill/fur.pkl')

# SG
sg = master[['sg']]
sg.to_pickle('dill/sg.pkl')

# ACTIVE EACH MONTH (no consideration for job changes or recall, only
# calculated on retirements of active employees as of start date)
emps_to_calc = master[master.line == 1].copy()
cmonths = f.career_months_df_in(emps_to_calc)
nonret_each_month = f.count_per_month(cmonths)
actives = pd.DataFrame(nonret_each_month, columns=['count'])
actives.to_pickle('dill/active_each_month.pkl')

# LIST ORDER PROPOSALS
# extract list ordering from a single Excel workbook containing proposed
# list orderings on separate worksheets
# The worksheet tab names are important for the function
# The pickle files will be named like the worbook sheet names
if cf.sample_mode:
    xl = pd.ExcelFile('sample_data/' + sample_prefix + 'proposals.xlsx')
else:
    xl = pd.ExcelFile('excel/proposals.xlsx')

sheets = xl.sheet_names
for ws in sheets:
    try:
        df = xl.parse(ws)
        df.set_index('empkey', inplace=True)
        df['idx'] = np.arange(len(df)).astype(int) + 1
        df.to_pickle('dill/' + ws + '.pkl')
    except:
        continue

# LAST MONTH
# percent of month for all days from starting date to the date of the last
# retirement.  Used for retirement month pay
dates = pd.date_range(cf.starting_date, master.retdate.max())
df_dates = pd.DataFrame(dates, columns=['dates'])
df_dates['day'] = df_dates.dates.apply(lambda x: x.day)
df_dates['lday'] = \
    df_dates.dates.apply(lambda x: (x + pd.offsets.MonthEnd(0)).day)
df_dates['last_pay'] = df_dates.day / df_dates.lday
df_dates.set_index('dates', inplace=True)
df_dates = df_dates[['last_pay']]
df_dates.to_pickle('dill/last_month.pkl')

