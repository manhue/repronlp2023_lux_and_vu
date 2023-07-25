import csv
import string


def create_random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

# Set a random seed for reproducibility
import random
random.seed('92331234659')

# Pretty printer
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Note the python version in case there is a change in shuffle algorithm
# - there is a difference in output between 2.7 and 3.6
import sys
print(sys.version)

# We will shuffle the pair within each item
systems = ['Tacotron', 'FastSpeech']
modes   = ['baseline', 'proposed']

# Create a list to store the order
experiment_order = []

# Create and shuffle
for i in range(1,7):
    for system in systems:
        arr = [f'{system}-{mode}-{i}' for mode in modes]
        random.shuffle(arr)
        experiment_order.append(arr)

random.shuffle(experiment_order)
pp.pprint(experiment_order)

# 3.6.9 (default, Jun 29 2022, 11:45:57)
# [GCC 8.4.0]
# [   ['FastSpeech-proposed-5', 'FastSpeech-baseline-5'],
#     ['FastSpeech-proposed-3', 'FastSpeech-baseline-3'],
#     ['Tacotron-proposed-6', 'Tacotron-baseline-6'],
#     ['FastSpeech-baseline-4', 'FastSpeech-proposed-4'],
#     ['FastSpeech-proposed-2', 'FastSpeech-baseline-2'],
#     ['Tacotron-proposed-1', 'Tacotron-baseline-1'],
#     ['Tacotron-proposed-4', 'Tacotron-baseline-4'],
#     ['FastSpeech-baseline-1', 'FastSpeech-proposed-1'],
#     ['Tacotron-proposed-5', 'Tacotron-baseline-5'],
#     ['Tacotron-proposed-2', 'Tacotron-baseline-2'],
#     ['Tacotron-proposed-3', 'Tacotron-baseline-3'],
#     ['FastSpeech-proposed-6', 'FastSpeech-baseline-6']]

# Create random string identifiers of length 4 for each video and output to CSV file
N = 4
header = ["video", "id"]
with open("video2id.csv", "w", newline='') as outf:
    csvwriter = csv.writer(outf)
    csvwriter.writerow(header)
    for a, b in experiment_order:
        csvwriter.writerow([a, create_random_string(N)])
        csvwriter.writerow([b, create_random_string(N)])

