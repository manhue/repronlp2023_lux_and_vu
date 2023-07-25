import pandas as pd

# process video info
video2id = pd.read_csv("../video2id.csv")
question2system = {}
question2order = {}

counter = 0
for _, rows in video2id.groupby(video2id.index // 2): # https://stackoverflow.com/a/57055020
    if "FastSpeech" in rows.iloc[0].video:
        question2system[counter] = "fastspeech"
    elif "Tacotron" in rows.iloc[0].video:
        question2system[counter] = "tacotron"

    if "proposed" in rows.iloc[0].video:
        question2order[counter] = ["proposed", "baseline"]
    else:
        question2order[counter] = ["baseline", "proposed"]
    counter += 1

# process survey results
survey_results = pd.read_csv("../survey_results/answers_gform.csv")

header = ["Person", "Question", "Encoding", "Method", "Preference", "Response"]
rows = [header]
user_id = 0
for _, user in survey_results[1:].iterrows():
    for question_idx, col in enumerate(survey_results.columns[2:]):
        outcome = user[col]
        if outcome == "Audio 1 und Audio 2 waren etwa gleich gut":
            response = 0
            answer = "equal"
        elif outcome == "Audio 1 ist deutlich besser als Audio 2":
             if question2order[question_idx][0] == "proposed":
                 response = 1
             else:
                response = 0
             answer = "A1 better"
        elif outcome == "Audio 2 ist deutlich besser als Audio 1":
            if question2order[question_idx][1] == "proposed":
                response = 1
            else:
                response = 0
            answer = "A2 better"
        else:
            continue # I think we can skip these? Could also filter them later (in R)

        if question2order[question_idx][0] == "proposed":
            encoding = "A1 {}, A2 baseline".format(question2system[question_idx])
        else:
            encoding = "A1 baseline, A2 {}".format(question2system[question_idx])

        rows.append([user_id, question_idx, encoding, question2system[question_idx], answer, response])
    user_id += 1

df = pd.DataFrame(rows)
df.to_csv("aggregated_form_data.csv", header=None, index=None)