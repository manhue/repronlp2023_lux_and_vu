import scipy.stats as scipy_stats
import math
import numpy as np
def small_sample_cv(set_of_set_of_measurements, labels=()):
    """
    Adapted from https://github.com/asbelz/coeff-var/blob/main/small_sample_cv.ipynb

    This code computes the coefficient of variation (CV) and some other stats for small samples (indicated by the * added to CV)
    for a given set of measurements which are assumed to be for the same or similar object, using the same measurand.
    Stats are adjusted for small sample size. Paper ref: Belz, Popovic & Mille (2022) Quantified Reproducibility Assessment of NLP Results,
    ACL'22.

    In this self-contained version, the set of measurements on which CV is computed is assigned to the variable set_of_set_of_measurements
    (see examples in code below).

    The reproducibility stats reported in the output are:
    * the unbiased coefficient of variation
    * the sample mean
    * the unbiased sample standard deviation with 95% confidence intervals, estimated on the basis of the standard error of the unbiassed sample variance
    * the sample size
    * the percentage of measured valued within two standard deviations
    * the percentage of measured valued within one standard deviation

    Example narrative output:

    The unbiased coefficient of variation is 1.5616560359100269 \
    for a mean of 85.58285714285714 , \
    unbiased sample standard deviation of 1.2904233075765223 with 95\% CI (0.4514829817654973, 2.1293636333875474) ,\
    and a sample size of 7 . \
    100.0 % of measured values fall within two standard deviations. \
    71.429 % of measured values fall within one standard deviation.

    NOTE:
    * CV assumes all measurements are positive; if they're not, shift measurement scale to start at 0
    * for fair comparison across studies, measurements on a scale that doesn't start at 0 need to be shifted to a scale that does start at 0

    KNOWN ISSUES:

    none
    """

    for idx, set_of_measurements in enumerate(set_of_set_of_measurements):
        if len(set_of_measurements) < 2:
            print(set_of_measurements, ": set of measurements is smaller than 2")
            break

        sample_mean = np.mean(set_of_measurements)
        if sample_mean <= 0:
            print(set_of_measurements, ": mean is 0 or negative")
            break

        sample_size = len(set_of_measurements)
        degrees_of_freedom = sample_size - 1
        sum_of_squared_differences = np.sum(np.square(sample_mean - set_of_measurements))

        # unbiassed sample variance s^2
        unbiassed_sample_variance = sum_of_squared_differences / degrees_of_freedom
        # corrected sample standard deviation s
        corrected_sample_standard_deviation = np.sqrt(unbiassed_sample_variance)
        # Gamma(N/2)
        gamma_N_over_2 = math.gamma(sample_size / 2)
        # Gamma((N-1)/2)
        gamma_df_over_2 = math.gamma(degrees_of_freedom / 2)
        # c_4(N)
        c_4_N = math.sqrt(2 / degrees_of_freedom) * gamma_N_over_2 / gamma_df_over_2
        # unbiassed sample std dev s/c_4
        unbiassed_sample_std_dev_s_c_4 = corrected_sample_standard_deviation / c_4_N
        # standard error of the unbiassed sample variance (assumes normally distributed population)
        standard_error_of_unbiassed_sample_variance = unbiassed_sample_variance * np.sqrt(2 / degrees_of_freedom)
        # estimated std err of std dev based on std err of unbiassed sample variance
        est_SE_of_SD_based_on_SE_of_unbiassed_sample_variance = standard_error_of_unbiassed_sample_variance / (
                2 * unbiassed_sample_std_dev_s_c_4)

        # COEFFICIENT OF VARIATION CV
        coefficient_of_variation = (unbiassed_sample_std_dev_s_c_4 / sample_mean) * 100
        # SMALL SAMPLE CORRECTED COEFFICIENT OF VARIATION CV*
        small_sample_coefficient_of_variation = (1 + (1 / (4 * sample_size))) * coefficient_of_variation

        # compute percentage of measured values within 1 and 2 standard deviations from the mean
        # initialise counts
        count_within_1_sd = 0
        count_within_2_sd = 0
        # for each measured value
        for m in set_of_measurements:
            # if it's within two std devs, increment count_within_2_sd
            if np.abs(m - sample_mean) < 2 * unbiassed_sample_std_dev_s_c_4:
                count_within_2_sd += 1
                # if it's also within one std devs, increment count_within_1_sd
                if np.abs(m - sample_mean) < unbiassed_sample_std_dev_s_c_4:
                    count_within_1_sd += 1

        # report results as described in code description above
        print("\n-----\n")
        if labels:
            print(">>> ", labels[idx])
        print("The unbiased coefficient of variation is", small_sample_coefficient_of_variation)
        print("for a mean of", sample_mean, ", ")
        print("unbiased sample standard deviation of", unbiassed_sample_std_dev_s_c_4, ", with 95\% CI",
              scipy_stats.t.interval(0.95, degrees_of_freedom, loc=unbiassed_sample_std_dev_s_c_4,
                                     scale=est_SE_of_SD_based_on_SE_of_unbiassed_sample_variance), ",")
        print("and a sample size of", sample_size, ".")
        print(count_within_2_sd / sample_size * 100, "% of measured values fall within two standard deviations.")
        print(round(count_within_1_sd / sample_size * 100, 3),
              "% of measured values fall within one standard deviation.")


# code copied from krippendorff_alpha.py at https://github.com/grrrr/krippendorff-alpha/blob/master/krippendorff_alpha.py
try:
    import numpy as np
except ImportError:
    np = None


def nominal_metric(a, b):
    return a != b


def interval_metric(a, b):
    return (a - b) ** 2


def ratio_metric(a, b):
    return ((a - b) / (a + b)) ** 2


def krippendorff_alpha(data, metric=interval_metric, force_vecmath=False, convert_items=float, missing_items=None):
    '''
    Calculate Krippendorff's alpha (inter-rater reliability):

    data is in the format
    [
        {unit1:value, unit2:value, ...},  # coder 1
        {unit1:value, unit3:value, ...},   # coder 2
        ...                            # more coders
    ]
    or
    it is a sequence of (masked) sequences (list, numpy.array, numpy.ma.array, e.g.) with rows corresponding to coders and columns to items

    metric: function calculating the pairwise distance
    force_vecmath: force vector math for custom metrics (numpy required)
    convert_items: function for the type conversion of items (default: float)
    missing_items: indicator for missing items (default: None)
    '''

    # number of coders
    m = len(data)

    # set of constants identifying missing values
    if missing_items is None:
        maskitems = []
    else:
        maskitems = list(missing_items)
    if np is not None:
        maskitems.append(np.ma.masked_singleton)

    # convert input data to a dict of items
    units = {}
    for d in data:
        try:
            # try if d behaves as a dict
            diter = d.items()
        except AttributeError:
            # sequence assumed for d
            diter = enumerate(d)

        for it, g in diter:
            if g not in maskitems:
                try:
                    its = units[it]
                except KeyError:
                    its = []
                    units[it] = its
                its.append(convert_items(g))

    units = dict((it, d) for it, d in units.items() if len(d) > 1)  # units with pairable values
    n = sum(len(pv) for pv in units.values())  # number of pairable values

    if n == 0:
        raise ValueError("No items to compare.")

    np_metric = (np is not None) and ((metric in (interval_metric, nominal_metric, ratio_metric)) or force_vecmath)

    Do = 0.
    for grades in units.values():
        if np_metric:
            gr = np.asarray(grades)
            Du = sum(np.sum(metric(gr, gri)) for gri in gr)
        else:
            Du = sum(metric(gi, gj) for gi in grades for gj in grades)
        Do += Du / float(len(grades) - 1)
    Do /= float(n)

    if Do == 0:
        return 1.

    De = 0.
    for g1 in units.values():
        if np_metric:
            d1 = np.asarray(g1)
            for g2 in units.values():
                De += sum(np.sum(metric(d1, gj)) for gj in g2)
        else:
            for g2 in units.values():
                De += sum(metric(gi, gj) for gi in g1 for gj in g2)
    De /= float(n * (n - 1))

    return 1. - Do / De if (Do and De) else 1.
## end copied code