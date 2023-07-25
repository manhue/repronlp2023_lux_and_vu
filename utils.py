import pandas as pd

def read_video_mapping(fname="video2id.csv"):
    video2id = pd.read_csv(fname)
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
        
    return question2system, question2order


