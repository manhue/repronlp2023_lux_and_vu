# ReproNLP 2023, Track C: Reproduction of human evaluation in Lux and Vu 2022
This repository contains code, data and information for our participation in the ReproNLP 2023 Shared Task, Track C, reproduction of evaluation in Lux &amp; Vu 2022.

## Directories
* _additional statistical analysis_:
  *  _plots_: generated boxplots and heatmaps
  * _aggregated_form_data.csv_: the survey form responses aggregated as preferences per system per person
  * _prepare_data_for_statistical_evaluation.py_: create file _aggregated_form_data.csv_ from _survey_results/answers_gform.csv_
  * _statistical_analysis.r_: R script to:
    * create boxplots and heatmaps
    * run binomial test
    * run linear mixed-effects model and calculate odds ratio

* _google_form_pdf_: contains a PDF export of the Google Form that was used for the survey

* _survey_results_: Google Form survey results, downloaded as CSV

## Files
* _compute_krippendorff_alpha.py_: compute interannotator agreement with krippendorff's alpha
* _compute_pearson_and_coefficient_of_variation.py_: compute Pearson correlations on type ii results and Coefficient of Variation on type i results
* _get_label_counts_from_raw_results.py_: calculate counts and percentages of each label category
* _random_videos.py_: create random ordering of videos for the Google Form (credits to Craig Thompson) and random identifiers for each video. This results in _video2id.csv_
* _stats.py_: statistical utilities
* _utils.py_: utilities for project-specific files
* _video2id.csv_: the result of running _random_videos.py_. The first column contains the video identification and the second column the anonymous identifier. The first two entries correspond to the videos used in the first survey question, the next two in the second question, etc.
