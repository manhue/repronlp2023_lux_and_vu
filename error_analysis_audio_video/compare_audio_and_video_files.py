import librosa
from librosa.feature import mfcc
import pandas as pd
import os
import re
import seaborn as sns
from matplotlib import pyplot as plt
from numpy.linalg import norm
import numpy as np
import scipy
from collections import defaultdict
"""
    Compare
        - original audio (this was validated against the files sent by the author)
        - created numbered video (1.mov, 2.mov, etc)
        - created final video with four-letter code

"""
audio_main_path = "audio_files/ACL_experiment_audios_German/"
video_main_path = "videos/"
video2id_path = "../video2id.csv"

video2id = pd.read_csv(video2id_path)

# Create MFCC features for each audio & video file
audio2mfcc = {}
video2mfcc = {}

n2audio = defaultdict(list)
n2video = defaultdict(list)

for _, row in video2id.iterrows():
    if "FastSpeech" in row.video:
        system = "fastspeech"
    elif "Tacotron" in row.video:
        system = "tacotron"

    if "proposed" in row.video:
        system_type = "proposed"
    elif "baseline" in row.video:
        system_type = "baseline"

    n = re.search("(\d)", row.video).group(1)
    path = os.path.join(audio_main_path, "Tacotron2" if system == "tacotron" else "Fastspeech2",
                        "Proposed" if system_type == "proposed" else "Baseline")
    audio = os.path.join(path, "{}_{}_{}.wav".format(system, system_type, n))
    numbered_video = os.path.join(path, "{}.mov".format(n))
    four_letter_video = os.path.join(video_main_path, "{}.mov".format(row.id))

    y_audio, sr_audio = librosa.load(audio)
    mfcc_audio = mfcc(y=y_audio, sr=sr_audio)
    audio2mfcc[audio] = mfcc_audio
    n2audio[n].append(audio)

    y_four_letter, sr_four_letter = librosa.load(four_letter_video)
    mfcc_four_letter = mfcc(y=y_four_letter, sr=sr_four_letter)
    video2mfcc[four_letter_video] = mfcc_four_letter # store with audio name, the one that we used
    n2video[n].append(four_letter_video)


# Do the comparison: L2 norm of difference between MFCC-vectors
table = [["audio", "video", "mean_cosine", "stdev_cosine"]]
outfolder = "heatmaps"
if not os.path.exists(outfolder):
    os.makedirs(outfolder, exist_ok=True)
for n in sorted(n2audio):
    results = []
    audios = n2audio[n]
    videos = n2video[n]
    for audio in audios:
        row = []
        mfcc_audio = audio2mfcc[audio]
        for video in videos:
            mfcc_video = video2mfcc[video]
            # cut to the length of the shorter file
            max_frame = min(mfcc_audio.shape[1], mfcc_video.shape[1]) - 1
            mfcc_audio_x = mfcc_audio[:, max_frame]
            mfcc_video_x = mfcc_video[:, max_frame]
            row.append(np.linalg.norm(mfcc_audio_x - mfcc_video_x))
        results.append(row)

    plt.clf()
    ax = sns.heatmap(results, cmap='RdYlGn_r', annot=True, cbar=False)
    audio_names_raw = [os.path.split(x)[1] for x in audios]
    audio_names = []
    for x in audio_names_raw:
        p1 = "Taco" if "tacotron" in x else "Fast"
        p2 = "Prop" if "proposed" in x else "Base"
        audio_names.append("{}-{}".format(p1, p2))
    ax.set(xlabel="Audio files", ylabel="Video files (hypothetical)",
           title="Distance between audio files and video files.",
           xticklabels=audio_names, yticklabels=audio_names)
    plt.savefig(os.path.join(outfolder, "sample{}_heatmap.png".format(n)))




