#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import math
import random
import numpy as np
import pandas as pd
import scipy.stats as st
from decimal import *
from pandas import ExcelFile
from pandas import ExcelWriter

df = pd.DataFrame(columns = ['experiment', 'pi_1', 'pi_2', 'pi_3', 'n_1', 'n_2', 'n_3', 'error','error_pre','z-score','z-score_pre','p-value','p-value_pre', 'effectsize', 'effectsize_pre', 'significant', 'significant_pre', 'ci_lower', 'ci_upper', 'ci_lower_pre', 'ci_upper_pre'])

#------- Set z-value for Confidence Interval according to pre-set alpha -------
alpha = 0.05
if alpha == 0.05:
	z_value = 1.96
elif alpha == 0.02:
	z_value = 2.32
elif alpha == 0.01:
	z_value = 2.57

#------- Variables -------
n_1 = 100
n_2 = 100
pi_1 = random.uniform(0., 1)
pi_2 = random.uniform(0., 1)
pi_3 = random.uniform(0., 1)

listpi_1 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
listpi_2 = [0, 0.001, 0.002, 0.01, 0.02, 0.1, 0.20, 0.25]

for i in range(len(listpi_1)):
	pi_1 = listpi_1[i]
	pi_3 = pi_1
	for x in range(len(listpi_2)):
		if (pi_1 + listpi_2[x] < 1.05):
			pi_2 = pi_1 + listpi_2[x]
			print pi_1, pi_2, pi_3

		#------- Loop over different sample sizes of pre-exp data -------
		steps = [10, 100, 1000]
		for x in range (0, len(steps)):
			n_3 = steps[x]	
			for i in range(0, 1000):
				flips = ['H' if (random.random() < pi_1) else 'T' for flipnr in xrange(n_1)]
				x_1 = flips.count('H')
				flips = ['H' if (random.random() < pi_3) else 'T' for flipnr in xrange(n_3)]
				x_3 = flips.count('H')
				flips = ['H' if (random.random() < pi_2) else 'T' for flipnr in xrange(n_2)]
				x_2 = flips.count('H')
				p_1 = x_1 / n_1
				p_2 = x_2 / n_2
				p_3 = x_3 / n_3

				x_1 = Decimal(x_1)
				x_2 = Decimal(x_2)
				x_3 = Decimal(x_3)
				n_3 = Decimal(n_3)
				n_1 = Decimal(n_1)
				n_2 = Decimal(n_2)

				pi =  (x_1+x_2)/(n_1+n_2) 
				pi_1_3 = (x_1 + x_3) / (n_1 + n_3)
				pi_1_2_3 = (x_1 + x_2 + x_3) / (n_1 + n_2 + n_3)
				
				pi_1_3 = Decimal(pi_1_3)
				pi_1_2_3 = Decimal(pi_1_2_3)
				p_3 = Decimal(p_3)
				p_2 = Decimal(p_2)
				p_1 = Decimal(p_1)
				pi = Decimal(pi)

				#------- Effect size -------
				effectsize = abs((p_2 - p_1))
				effectsize_pre = abs((p_2 - pi_1_3))

				#------- Error + z-test -------
				error = math.sqrt((pi*(1-pi))*(1/n_1 + 1/n_2)) 
				error_pre = math.sqrt((pi_1_3*(1-pi_1_3))*(1/(n_1+n_3) + 1/n_2))
				zscore = (p_1 - p_2) / Decimal(error)
				zscore_pre = (pi_1_3 - p_2) / Decimal(error_pre)
				pval = st.norm.sf(abs(float(zscore)))*2
				pval_pre = st.norm.sf(abs(float(zscore_pre)))*2

				significant = 0
				significant_pre = 0
				if pval < alpha:
					significant = 1
				if pval_pre < alpha:
					significant_pre = 1

				#------- Confidence interval for 95%, 98% or 99% -------
				ci_lower = (p_1 - p_2) + Decimal(z_value*error)
				ci_upper = (p_1 - p_2) - Decimal(z_value*error)
				ci_lower_pre = (pi_1_3 - p_2) + Decimal(z_value*error_pre)
				ci_upper_pre = (pi_1_3 - p_2) - Decimal(z_value*error_pre)

				#------- Write data to data frame -------
				df.loc[len(df)] = [Decimal(x), pi_1, pi_2, pi_3, n_1, n_2, n_3, error, error_pre, zscore, zscore_pre, pval, pval_pre, effectsize, effectsize_pre, significant, significant_pre, ci_lower, ci_upper, ci_lower_pre, ci_upper_pre]

writer = ExcelWriter('df.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()