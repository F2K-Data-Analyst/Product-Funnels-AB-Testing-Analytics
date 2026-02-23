#%%
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
#%%
def conversion_test(success_a, total_a, success_b, total_b):
    count = np.array([success_a, success_b])
    nobs = np.array([total_a, total_b])

    stat, pval = proportions_ztest(count, nobs)
    return stat, pval