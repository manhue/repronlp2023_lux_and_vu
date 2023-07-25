import pandas as pd
from collections import defaultdict
import utils

# process video info
video2id = pd.read_csv("video2id.csv")
question2system, question2order = utils.read_video_mapping()

# process survey results
survey_results = pd.read_csv("survey_results/answers_gform.csv")
results_tacotron = defaultdict(int)
results_fastspeech = defaultdict(int)

for _, user in survey_results[1:].iterrows():
    for idx, col in enumerate(survey_results.columns[2:]):
        outcome = user[col]
        if outcome == "Audio 1 und Audio 2 waren etwa gleich gut":
            result = "both"
        elif outcome == "Audio 1 ist deutlich besser als Audio 2":
             result = question2order[idx][0]
        elif outcome == "Audio 2 ist deutlich besser als Audio 1":
            result = question2order[idx][1]
        else:
            result = "skip"

        if question2system[idx] == "tacotron":
            results_tacotron[result] += 1
        else:
            results_fastspeech[result] += 1

print(question2system)
print("Fastspeech:", results_fastspeech)
print("Tacotron:", results_tacotron)

