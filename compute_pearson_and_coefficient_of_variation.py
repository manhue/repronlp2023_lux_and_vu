from stats import small_sample_cv
from scipy import stats as scipy_stats

# raw preference scores: baseline, proposed, equal
scores_taco_orig = [22, 106, 76]
scores_taco_repro = [274, 271, 391] # omit 6 skipped

scores_fastspeech_orig = [63, 51, 88]
scores_fastspeech_repro = [113, 471, 358]

scores_all_orig = [22, 106, 76, 63, 51, 88]
scores_all_repro = [274, 271, 391, 113, 471, 358]
scores_all_repro_transposed = [113, 471, 358, 274, 271, 391]

# Pearson
print("### Pearson correlation")
print("Pearson Original x Reproduced: ", scipy_stats.pearsonr(scores_all_orig, scores_all_repro))
print("Pearson Fastspeech-orig x Fastspeech repro:", scipy_stats.pearsonr(scores_fastspeech_orig, scores_fastspeech_repro))
print("Pearson Pearson Taco-orig x Taco repro:", scipy_stats.pearsonr(scores_taco_orig, scores_taco_repro))

# Pearson Original x Reproduced:  PearsonRResult(statistic=0.001978170989445763, pvalue=0.9970327473862817)
# Pearson Fastspeech-orig x Fastspeech repro: PearsonRResult(statistic=-0.11346993786539811, pvalue=0.9276068747553574)
# Pearson Taco-orig x Taco repro: PearsonRResult(statistic=0.14109143361714005, pvalue=0.9098776920074706)


print("\n")
# what if it was flipped?

print("Pearson Original x Reproduced Transposed:", scipy_stats.pearsonr(scores_all_orig, scores_all_repro_transposed))
print("Pearson Taco-orig x Fastspeech repro (i.e. if transposed):", scipy_stats.pearsonr(scores_taco_orig, scores_fastspeech_repro))
print("Pearson Fastspeech-orig x Taco repro (i.e. if transposed):", scipy_stats.pearsonr(scores_fastspeech_orig, scores_taco_repro))

# Pearson Original x Reproduced Transposed: PearsonRResult(statistic=0.990898818129858, pvalue=0.0001238703348250313)
# Pearson Taco-orig x Fastspeech repro (i.e. if transposed): PearsonRResult(statistic=0.9989301126035575, pvalue=0.0294511925177622)
# Pearson Fastspeech-orig x Taco repro (i.e. if transposed): PearsonRResult(statistic=0.9548801155844335, pvalue=0.19196662575493664)




# Coefficient of Variation

set_of_set_of_measurements = [[63, 113], # Fastspeech-baseline
                              [51, 471], # Fastspeech-lowresource
                              [88, 359], # Fastspeech-equal
                              [22, 274], # Tacotron-baseline
                              [106, 271],  # Tacotron-lowresource
                              [76, 391]]  # Tacotron-equal

set_of_set_of_measurements_percentages = [[31, 12], # Fastspeech-baseline
                              [25, 50], # Fastspeech-lowresource
                              [43, 38], # Fastspeech-equal
                              [11, 29], # Tacotron-baseline
                              [52, 29],  # Tacotron-lowresource
                              [37, 41]]  # Tacotron-equal

labels = ["Fastspeech-baseline", "Fastspeech-lowresource", "Fastspeech-equal",
          "Tacotron-baseline", "Tacotron-lowresource", "Tacotron-equal"]


set_of_set_of_measurements_transposed = [[63, 274],
                                         [51, 271],
                                         [88, 391],
                                         [22, 113],
                                         [106, 471],
                                         [76, 358]]


set_of_set_of_measurements_transposed_percentages = \
                              [[31, 29],
                              [25, 29],
                              [43, 41],
                              [11,  12],
                              [52, 50 ],
                              [37, 38]]


labels_transposed = ["FS orig x Taco repro Baseline", "FS orig x Taco Repro Low Res", "FS Orig x Taco Repro Equal",
                     "Taco orig x FS repro Baseline", "Taco orig x FS repro Low Resource", "Taco orig x FS repro Equal"]


print("\n\n\n### Coefficient of Variation")
small_sample_cv(set_of_set_of_measurements_percentages, labels)
# >>>  Fastspeech-baseline
# The unbiased coefficient of variation is 88.10744433280324
# for a mean of 21.5 ,
# unbiased sample standard deviation of 16.838311583602398 , with 95\% CI (-79.47349197959204, 113.15011514679682) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  Fastspeech-lowresource
# The unbiased coefficient of variation is 66.46701940895684
# for a mean of 37.5 ,
# unbiased sample standard deviation of 22.155673136318946 , with 95\% CI (-104.57038418367372, 148.88173045631163) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  Fastspeech-equal
# The unbiased coefficient of variation is 12.30870729795497
# for a mean of 40.5 ,
# unbiased sample standard deviation of 4.4311346272637895 , with 95\% CI (-20.914076836734736, 29.77634609126232) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  Tacotron-baseline
# The unbiased coefficient of variation is 89.73047620209174
# for a mean of 20.0 ,
# unbiased sample standard deviation of 15.95208465814964 , with 95\% CI (-75.29067661224508, 107.19484592854437) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  Tacotron-lowresource
# The unbiased coefficient of variation is 56.62005357059286
# for a mean of 40.5 ,
# unbiased sample standard deviation of 20.38321928541343 , with 95\% CI (-96.20475344897983, 136.9711920198067) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  Tacotron-equal
# The unbiased coefficient of variation is 10.22569529368567
# for a mean of 39.0 ,
# unbiased sample standard deviation of 3.5449077018110318 , with 95\% CI (-16.731261469387793, 23.821076873009854) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.


print("\n\n\n### Coefficient of Variation - transposed")
small_sample_cv(set_of_set_of_measurements_transposed_percentages, labels_transposed)
# >>>  FS orig x Taco repro Baseline
# The unbiased coefficient of variation is 6.646701940895685
# for a mean of 30.0 ,
# unbiased sample standard deviation of 1.7724538509055159 , with 95\% CI (-8.365630734693896, 11.910538436504927) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  FS orig x Taco Repro Low Res
# The unbiased coefficient of variation is 14.770448757545966
# for a mean of 27.0 ,
# unbiased sample standard deviation of 3.5449077018110318 , with 95\% CI (-16.731261469387793, 23.821076873009854) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  FS Orig x Taco Repro Equal
# The unbiased coefficient of variation is 4.747644243496918
# for a mean of 42.0 ,
# unbiased sample standard deviation of 1.7724538509055159 , with 95\% CI (-8.365630734693896, 11.910538436504927) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  Taco orig x FS repro Baseline
# The unbiased coefficient of variation is 8.669611227255242
# for a mean of 11.5 ,
# unbiased sample standard deviation of 0.8862269254527579 , with 95\% CI (-4.182815367346948, 5.955269218252464) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  Taco orig x FS repro Low Resource
# The unbiased coefficient of variation is 3.909824671115109
# for a mean of 51.0 ,
# unbiased sample standard deviation of 1.7724538509055159 , with 95\% CI (-8.365630734693896, 11.910538436504927) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.
#
# -----
#
# >>>  Taco orig x FS repro Equal
# The unbiased coefficient of variation is 2.6586807763582736
# for a mean of 37.5 ,
# unbiased sample standard deviation of 0.8862269254527579 , with 95\% CI (-4.182815367346948, 5.955269218252464) ,
# and a sample size of 2 .
# 100.0 % of measured values fall within two standard deviations.
# 100.0 % of measured values fall within one standard deviation.



