# -*- coding: utf-8 -*-

'''Merge and order a master dataframe containing all employees (including
inactive employees), with a proposed list dataframe which may contain all
employees or only active (and optionally furloughed) employees.

If the proposed list ordering does not contain the inactive employees, the
'fill_style' argument determines where the inactive employees will be
placed within the combined list relative to their same employee group
active cohorts, just senior to the closest junior cohort or just junior to
closest senior cohort.

Writes results to a pickle file and an Excel file.

example jupyter notebook usage:
    %run join_inactives.py master p1 final bfill
'''

import pandas as pd
import numpy as np
import config as cf

from sys import argv

script, master_name, proposed_order_df, output_name, fill_style = argv

pre, suf = 'dill/', '.pkl'
xlpre, xlsuf = 'reports/', '.xlsx'

if cf.sample_mode:
    output_name = cf.sample_prefix + output_name


master_path_string = (pre + master_name + suf)
order_path_string = (pre + proposed_order_df + suf)
write_xl_path = (xlpre + output_name + xlsuf)

df_master = pd.read_pickle(master_path_string)
df_order = pd.read_pickle(order_path_string)

joined = df_master.join(df_order, how='outer')

eg_set = np.unique(joined.eg)

final = pd.DataFrame()

for eg in eg_set:

    eg_df = joined[joined.eg == eg].copy()
    eg_df.sort_values('eg_order', inplace=True)

    if fill_style == 'ffill':
        eg_df.iloc[0, eg_df.columns.get_loc('idx')] = eg_df.idx.min()
        eg_df.idx = eg_df.idx.fillna(method='ffill').astype(int)

    if fill_style == 'bfill':
        eg_df.iloc[-1, eg_df.columns.get_loc('idx')] = eg_df.idx.max()
        eg_df.idx = eg_df.idx.fillna(method='bfill')  # .astype(int)

    final = pd.concat([final, eg_df])

final = final.sort_values(['idx', 'eg_order'])
final['snum'] = np.arange(len(final)).astype(int) + 1
final.pop('idx')

final.to_pickle('dill/' + output_name + '.pkl')

final.set_index('snum', drop=True, inplace=True)

writer = pd.ExcelWriter(write_xl_path,
                        engine='xlsxwriter',
                        datetime_format='yyyy-mm-dd',
                        date_format='yyyy-mm-dd')

final.to_excel(writer, sheet_name='final')
writer.save()
