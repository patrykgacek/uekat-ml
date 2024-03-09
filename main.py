import csv
import os

def load_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def count_occur(data):
    hist = []
    
    # Init list with attributes names from first row
    for attr in data[0]:
        hist.append({attr: 0})

    # Count occurances of each attribute
    for row in data:
        for idx_attr, attr in enumerate(row):
            if attr in hist[idx_attr]:
                hist[idx_attr][attr] = hist[idx_attr][attr] + 1
            else:
                hist[idx_attr][attr] = 1

    return hist



files = os.listdir('data')
for file in files:
    data = load_data('data/' + file)
    histogram = count_occur(data)
    print(file, histogram)
