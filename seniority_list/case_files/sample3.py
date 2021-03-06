# -*- coding: utf-8 -*-

from config import enhanced_jobs
from pandas import to_datetime
from collections import OrderedDict as od

full_time_pcnt1 = .6
full_time_pcnt2 = .65
full_time_avg_pcnt = (full_time_pcnt1 + full_time_pcnt2) / 2

top_of_scale = 12

pay_table_exception_year = 2014.1
date_exception_start = '2014-12-31'
date_exception_end = '2014-12-31'

future_raise = False
last_contract_year = 2019.0
annual_pcnt_raise = .02

# INDEXED PAY TABLE GENERATION INPUTS
pay_table_year_sort = 2018.0
pay_table_longevity_sort = 7
enhanced_jobs_full_suffix = 'B'
enhanced_jobs_part_suffix = 'R'

init_ret_age_years = 65
init_ret_age_months = 0

init_ret_age = init_ret_age_years + (init_ret_age_months * 1 / 12)
ret_age_increase = False
# format for ret_incr:
# ((end of effective month, age increase in months))
# all employees in effective month will not retire and will have
# retirement date adjusted
ret_incr = (('2018-01-31', 12),
            ('2020-01-31', 12))

ret_incr_dict = od(ret_incr)

if ret_age_increase:
    ret_age = init_ret_age + sum(ret_incr_dict.values()) * (1 / 12)
else:
    ret_age = init_ret_age

starting_date = '2013-12-31'
start = to_datetime(starting_date)

implementation_date = '2016-10-31'
imp_date = to_datetime(implementation_date)
imp_month = ((imp_date.year - start.year) * 12) - \
    (start.month - imp_date.month)

end_date = to_datetime('2020-01-31')
ratio_final_month = ((end_date.year - start.year) * 12) - \
    (start.month - end_date.month)

# NUMBER OF JOB LEVELS, CONVERSION DATA
# (basic to enhanced)
if enhanced_jobs:
    num_of_job_levels = 16

    # Job dictionary for enhanced jobs conversion:
    # full_time_pcnt1/2 represent different percentages of full-time positions
    jd = {
        1: [1, 2, full_time_pcnt1],
        2: [3, 5, full_time_avg_pcnt],
        3: [4, 6, full_time_pcnt2],
        4: [7, 8, full_time_pcnt1],
        5: [9, 12, full_time_avg_pcnt],
        6: [10, 13, full_time_pcnt2],
        7: [11, 14, full_time_pcnt2],
        8: [15, 16, full_time_pcnt2]
    }
else:
    num_of_job_levels = 8

# JOB COUNTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
eg1_job_count = [197, 470, 1056, 412, 628, 1121, 0, 0]
eg2_job_count = [80, 85, 443, 163, 96, 464, 54, 66]
eg3_job_count = [0, 26, 319, 0, 37, 304, 0, 0]
furlough_count = [340, 0, 23]

# JOB CHANGES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# [job level affected, [start and end month], total change,
# [standalone allocation]]
# group 4 additions...
jc1 = [1, [35, 64], 43, [40, 3, 0]]
jc2 = [4, [35, 64], 72, [66, 6, 0]]
# group3 reductions...
jc3 = [2, [1, 52], -408, [-377, -23, -8]]
jc4 = [5, [1, 52], -510, [-474, -26, -10]]
# group 2 additions...
jc5 = [3, [1, 61], 411, [376, 26, 9]]
jc6 = [6, [1, 61], 411, [376, 26, 9]]

j_changes = [jc1, jc2, jc3, jc4, jc5, jc6]
eg_counts = [eg1_job_count, eg2_job_count, eg3_job_count]

# RECALLS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# [total monthly_recall_count, eg recall allocation,
#   start_month, end_month]
recall_1 = [8, [6, 0, 2], 50, 75]
recall_2 = [10, [10, 0, 0], 75, 150]

recalls = [recall_1, recall_2]

# CONDITION DATA
if enhanced_jobs:
    # sg prex award (all reserve...)  TODO - make function
    # sequence = [eg, jnum, count, start_month, end_month]
    sg1 = [1, 5, 43, 0, 67]
    sg2 = [1, 6, 130, 0, 67]
    sg3 = [1, 12, 43, 0, 67]
    sg4 = [1, 13, 130, 0, 67]

    # ratio condition
    # sequence = [eg, jnum, pcnt, start_month, end_month]
    r1 = [1, 1, imp_month, ratio_final_month]
    r2 = [1, 2, imp_month, ratio_final_month]
    r3 = [1, 7, imp_month, ratio_final_month]
    r4 = [1, 8, imp_month, ratio_final_month]

    # count-capped ratio condition
    # sequence = [eg, jnum, count, start_month, end_month]
    c1 = [2, 1, 55, imp_month, imp_month + 60]
    c2 = [2, 2, 37, imp_month, imp_month + 60]
    c3 = [2, 7, 101, imp_month, imp_month + 60]
    c4 = [2, 8, 67, imp_month, imp_month + 60]

    # dict below is input for assign_cond_ratio_capped function
    # sequence = (job, enhanced_jobs): ([weights, capped limit, job pcnt])
    # the job pcnt input is used with enhanced jobs (divides capped limit
    # into full/part time level cap)
    quota_dict = {(1, 1): ([2.48, 1], 320, full_time_pcnt1),
                  (2, 1): ([2.48, 1], 320, 1 - full_time_pcnt1),
                  (7, 1): ([2.46, 1], 580, full_time_pcnt1),
                  (8, 1): ([2.46, 1], 580, 1 - full_time_pcnt1),
                  (1, 0): ([2.48, 1], 320, 1),
                  (4, 0): ([2.46, 1], 580, 1)}

    sg_rights = [sg1, sg2, sg3, sg4]
    ratio_cond = [r1, r2, r3, r4]
    count_cond = [c1, c2, c3, c4]

else:

    # sg prex award (all reserve...)
    # sequence = [eg, jnum, count, start_month, end_month]
    sg1 = [1, 2, 43, 0, 67]
    sg2 = [1, 3, 130, 0, 67]
    sg3 = [1, 5, 43, 0, 67]
    sg4 = [1, 6, 130, 0, 67]

    # ratio condition
    # sequence = [eg, jnum, pcnt, start_month, end_month]
    r1 = [1, 1, imp_month, ratio_final_month]
    r2 = [1, 4, imp_month, ratio_final_month]

    # count-capped ratio condition
    # sequence = [eg, jnum, count, start_month, end_month]
    c1 = [2, 1, 92, imp_month, imp_month + 60]
    c2 = [2, 4, 168, imp_month, imp_month + 60]

    # dict below is input for assign_cond_ratio_capped function
    # sequence = (job, enhanced_jobs): ([weights, capped limit, job pcnt])
    # the job pcnt input is used with enhanced jobs (divides capped limit
    # into full/part time level cap)
    quota_dict = {(1, 1): ([2.48, 1], 320, full_time_pcnt1),
                  (2, 1): ([2.48, 1], 320, 1 - full_time_pcnt1),
                  (7, 1): ([2.46, 1], 580, full_time_pcnt1),
                  (8, 1): ([2.46, 1], 580, 1 - full_time_pcnt1),
                  (1, 0): ([2.48, 1], 320, 1),
                  (4, 0): ([2.46, 1], 580, 1)}

    sg_rights = [sg1, sg2, sg3, sg4]
    ratio_cond = [r1, r2]
    count_cond = [c1, c2]

# DICTIONARIES, DESCRIPTIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
eg_dict = {1: '1', 2: '2', 3: '3', 4: 'sa'}
eg_dict_verbose = {1: 'Group 1', 2: 'Group 2', 3: 'Group 3',
                   4: 'Standalone'}
proposal_dict = {'ds1': 'Group 1 Proposal', 'ds2': 'Group 2 Proposal',
                 'ds3': 'Group 3 Proposal', 'ds4': 'Standalone Data'}

# detailed job labels...
if enhanced_jobs:

    job_strs = ['Capt G4 B', 'Capt G4 R', 'Capt G3 B', 'Capt G2 B',
                'Capt G3 R', 'Capt G2 R', 'F/O  G4 B', 'F/O  G4 R',
                'F/O  G3 B', 'F/O  G2 B', 'Capt G1 B', 'F/O  G3 R',
                'F/O  G2 R', 'Capt G1 R', 'F/O  G1 B', 'F/O  G1 R', 'FUR']

    jobs_dict = {1: 'Capt G4 B', 2: 'Capt G4 R', 3: 'Capt G3 B',
                 4: 'Capt G2 B', 5: 'Capt G3 R', 6: 'Capt G2 R',
                 7: 'F/O  G4 B', 8: 'F/O  G4 R', 9: 'F/O  G3 B',
                 10: 'F/O  G2 B', 11: 'Capt G1 B', 12: 'F/O  G3 R',
                 13: 'F/O  G2 R', 14: 'Capt G1 R', 15: 'F/O  G1 B',
                 16: 'F/O  G1 R', 17: 'FUR'}

# basic job labels...
else:

    job_strs = ['Capt G4', 'Capt G3', 'Capt G2', 'F/O  G4', 'F/O  G3',
                'F/O  G2', 'Capt G1', 'F/O  G1', 'FUR']

    jobs_dict = {1: 'Capt G4', 2: 'Capt G3', 3: 'Capt G2', 4: 'F/O  G4',
                 5: 'F/O  G3', 6: 'F/O  G2', 7: 'Capt G1', 8: 'F/O  G1',
                 9: 'FUR'}

# CHART COLORS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

if enhanced_jobs:  # enhanced job level chart colors (16)

    grp1_color = ['#008f00', '#006600', '#7b1979', '#0433ff', '#551154',
                  '#4d6dff', '#ff7c00', '#ffa34d', '#ff2600', '#fffb00',
                  '#9ec2e9', '#ff8080', '#fffd99', '#c1d8f1', '#e2a8a5',
                  '#f3dad8', '#ffb3ff']

    grp2_color = ['#5091cf', '#2492f9', '#b33932', '#9aba5a', '#da160b',
                  '#88cc00', '#00b2ec', '#37cafb', '#b0a2cb', '#b6dde9',
                  '#ef994d', '#a57ef1', '#a6b9bf', '#ffa64d', '#c7bb9a',
                  '#c8b79d', '#fefc05']

    grp3_color = ['#3064a4', '#3399ff', '#aa322f', '#81a33a', '#ff1a1a',
                  '#88cc00', '#66488a', '#9679b9', '#2c93af', '#dd7621',
                  '#7b95c1', '#5cbcd6', '#e89f64', '#ffa64d', '#c67c7b',
                  '#c8b79d', '#fefc05']

    color_lists = [grp1_color, grp2_color, grp3_color]

    job_colors = [
        [0.65, 0.81, 0.89, 1.0],
        [0.31, 0.59, 0.77, 1.0],
        [0.19, 0.39, 0.7, 1.0],
        [0.66, 0.85, 0.55, 1.0],
        [0.41, 0.73, 0.32, 1.0],
        [0.22, 0.6, 0.23, 1.0],
        [0.93, 0.61, 0.57, 1.0],
        [0.93, 0.32, 0.32, 1.0],
        [0.75, 0.1, 0.1, 1.0],
        [0.99, 0.79, 0.49, 1.0],
        [0.95, 0.65, 0.19, 1.0],
        [0.82, 0.42, 0.12, 1.0],
        [0.82, 0.67, 0.71, 1.0],
        [0.6, 0.47, 0.72, 1.0],
        [0.5, 0.35, 0.6, 1.0],
        [0.9, 0.87, 0.6, 1.0]]

else:  # basic 8-level chart colors

    grp1_color = ['#008f00', '#7b1979', '#0433ff', '#ff7c00', '#ff2600',
                  '#fffb00', '#9ec2e9', '#e2a8a5', '#ffb3ff']

    grp2_color = ['#5091cf', '#b33932', '#9aba5a', '#00b2ec', '#b0a2cb',
                  '#b6dde9', '#ef994d', '#c7bb9a', '#fefc05']

    grp3_color = ['#3064a4', '#aa322f', '#81a33a', '#66488a', '#2c93af',
                  '#dd7621', '#7b95c1', '#c67c7b', '#fefc05']

    color_lists = [grp1_color, grp2_color, grp3_color]

    job_colors = [[0.65, 0.8, 0.89, 1.],
                  [0.14, 0.48, 0.7, 1.],
                  [0.66, 0.85, 0.51, 1.],
                  [0.28, 0.62, 0.21, 1.],
                  [0.97, 0.53, 0.53, 1.],
                  [0.9, 0.21, 0.16, 1.],
                  [0.99, 0.79, 0.49, 1.],
                  [0.94, 0.54, 0.2, 1.]]

eg_colors = ['#505050', '#0081ff', '#ff6600']

lin_reg_colors = ['#00b300', '#0086b3', '#cc5200']
lin_reg_colors2 = ['grey', '#0086b3', '#cc5200']
mean_colors = ['#4d4d4d', '#3399ff', '#ff8000']

# alternate white, grey
white_grey = ['#999999', '#ffffff', '#999999', '#ffffff', '#999999',
              '#ffffff', '#999999', '#ffffff', '#999999', '#ffffff',
              '#999999', '#ffffff', '#999999', '#ffffff', '#999999',
              '#ffffff', '#999999']

color1 = ['#00ff00', '#80ff80', '#cc3300', '#005ce6', '#ff8c66',
          '#3384ff', '#00ff00', '#80ff80', '#cc3300', '#005ce6',
          '#ffff00', '#ff8c66', '#3384ff', '#ffff00', '#e600e5',
          '#ff66fe', '#ff0000']

color2 = ['#ff0066', '#ff4d94', '#ffff00', '#00b2b3', '#ffff99',
          '#00e4e6', '#ff0066', '#ff4d94', '#ffff00', '#00b2b3',
          '#6600cc', '#ffff99', '#00e4e6', '#ffff00', '#8c1aff',
          '#8c1aff', '#ff0000']

color3 = ['#ff0066', '#ff4d94', '#0033cc', '#ffff00', '#0040ff',
          '#ffff99', '#ff0066', '#ff4d94', '#0033cc', '#ffff00',
          '#00cc00', '#0040ff', '#ffff99', '#00e600', '#00cc00',
          '#00e600', '#333333']

# CHART LABEL ADJUSTMENT
# for chart lable adjustment (secondary y label positioning)
if enhanced_jobs:
    adjust = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -75, 50, 0, -160, -40, 120, 0]
else:
    adjust = [0, 0, 0, 0, 0, 0, -50, 50, 0]

# reference only:

# job_num,job_code
# 1.0,c4b
# 2.0,c4r
# 3.0,c3b
# 4.0,c2b
# 5.0,c3r
# 6.0,c2r
# 7.0,f4b
# 8.0,f4r
# 9.0,f3b
# 10.0,f2b
# 11.0,c1b
# 12.0,f3r
# 13.0,f2r
# 14.0,c1r
# 15.0,f1b
# 16.0,f1r

# job_num,job_code
# 1.0,c4
# 2.0,c3
# 3.0,c2
# 4.0,f4
# 5.0,f3
# 6.0,f2
# 7.0,c1
# 8.0,f1
