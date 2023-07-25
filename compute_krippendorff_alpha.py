import pandas as pd
import utils
import stats

question2system, _ = utils.process_video_mapping()

# process survey results
survey_results = pd.read_csv("survey_results/answers_gform.csv")

all_rows = []
rows = []
outcomes = {'Audio 1 ist deutlich besser als Audio 2': 0,
            'Audio 2 ist deutlich besser als Audio 1': 1,
            'Audio 1 und Audio 2 waren etwa gleich gut': 2}

missing_label = '*'

for _, user in survey_results[1:].iterrows():
    row = []
    missing = False
    for _, col in enumerate(survey_results.columns[2:]):
        outcome = user[col]
        if not outcome in outcomes.keys():
            missing = True
            row.append(missing_label)
        else:
            row.append(outcomes[outcome])

    if not missing:
        rows.append(row)

    all_rows.append(row)


# split by system
tacotron_responses = []
fastspeech_responses = []
for user_answers in all_rows:
    tr = []
    fr = []
    for idx, response in enumerate(user_answers):
        if question2system[idx] == "tacotron":
            tr.append(response)
        elif question2system[idx] == "fastspeech":
            fr.append(response)

    tacotron_responses.append(tr)
    fastspeech_responses.append(fr)


print(stats.krippendorff_alpha(all_rows, metric=stats.nominal_metric, missing_items=missing_label)) # 0.11752534562060091
print(stats.krippendorff_alpha(tacotron_responses, metric=stats.nominal_metric, missing_items=missing_label)) # 0.05494425116231516
print(stats.krippendorff_alpha(fastspeech_responses, metric=stats.nominal_metric, missing_items=missing_label)) # 0.1782336078664556
print(stats.krippendorff_alpha(rows, metric=stats.nominal_metric, missing_items=missing_label)) # 0.11971738161650125