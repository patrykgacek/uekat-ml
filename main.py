import os


# Load data from file
def load_data(filename):
    data = []
    with open(filename, "r") as f:
        for line in f:
            row = line.strip().split(",")
            data.append(row)
    return data


# Count occurances of each attribute
# Returns [{attr1: count1, attr2: count2, ...}, ...]
def count_occur(data):
    # Init list with attributes names from first row
    hist = []
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


# Distinct attribute names
# Returns [[attr1, attr2, ...], ...]
def get_distinct_attr(data):
    # Init list with attributes names from first row
    distinct = []
    for attr in data[0]:
        distinct.append([attr])

    for row in data:
        for idx_attr, attr in enumerate(row):
            if attr not in distinct[idx_attr]:
                distinct[idx_attr].append(attr)

    return distinct


# Count the occurrences of an attribute for decision
# Returns [{attr1: {decision1: count1, decision2: count2, ...}, ...}, ...]
def count_occur_decision(data, attributes):
    # Init decision dictionary
    decision_init = {}
    for row in attributes[-1]:
        decision_init[row] = 0

    # Init decision list
    decisions = []
    for idx_row, row in enumerate(attributes[0:-1]):
        decisions.append({})
        for attr in row:
            decisions[idx_row][attr] = decision_init.copy()

    # Count occurances of each attribute for decision
    for row in data:
        for idx_attr, attr in enumerate(row[0:-1]):
            decisions[idx_attr][attr][row[-1]] = decisions[idx_attr][attr][row[-1]] + 1

    return decisions


# Newton-Raphson method for logarithm calculation with base 2
# Returns log2(x)
def log2(x, epsilon=1e-15):
    if x < 0:
        return float("nan")

    if x == 0:
        return float("-inf")

    if x == 1:
        return 0

    n = 1.0
    ln2 = 0.6931471805599453  # ln(2)
    while abs(2**n - x) > epsilon:
        # 2**n * ln(2) is the derivative of 2**n
        n -= (2**n - x) / (2**n * ln2)
    return n


# Calculate entropy
# Returns Info(T)
def info(dictionary):
    # Calculate total number of occurances
    total = 0
    for key in dictionary:
        total = total + dictionary[key]

    # Calculate entropy
    entropy = 0
    for key in dictionary:
        p = dictionary[key] / total
        if p > 0:
            entropy = entropy - p * log2(p)

    return entropy


# Calculate entropy for attribute
# Returns Info(a, T)
def info_attr(decisions, attributes, histogram, total):
    attr_entropy = 0
    for attr in attributes:
        p = histogram[attr] / total
        attr_entropy = attr_entropy + p * info(decisions[attr])

    return attr_entropy


# List of entropy for each attribute
# Returns [Info(a1, T), Info(a2, T), ...]
def info_attrs(decisions, attributes, histogram, total):
    attrs_entropy = []
    for idx_attr, attr in enumerate(attributes):
        attrs_entropy.append(
            info_attr(decisions[idx_attr], attr, histogram[idx_attr], total)
        )
    return attrs_entropy


# Calculate gain for attribute
# Returns Gain(a, T)
def gain_attr(info, info_attr):
    return info - info_attr


# List of gain for each attribute
# Returns [Gain(a1, T), Gain(a2, T), ...]
def gain_attrs(info, attrs_entropy):
    gains = []
    for attr_entropy in attrs_entropy:
        gains.append(gain_attr(info, attr_entropy))
    return gains


# Print
def print_rows(data, padding=2, max_rows=1000):
    # Calculate max length for each attribute
    max_len = []
    for idx, attr in enumerate(data[0]):
        max_len.append(len(attr))

    for attr in data:
        for idx, a in enumerate(attr):
            if max_len[idx] < len(a):
                max_len[idx] = len(a)

    max_len = [x + padding for x in max_len]
    sum_len = sum(max_len) + padding + 1

    # Print header
    print("[", end="".rjust(padding, " "))
    for idx, attr in enumerate(data[0]):
        print(f"a{idx + 1}".ljust(max_len[idx], " "), end="")
    print("]")

    # Print separator
    print("[".ljust(sum_len, "-"), end="]\n")

    # Print rows
    for row in data[:max_rows]:
        print("[", end="".rjust(padding, " "))
        for idx, attr in enumerate(row):
            print(f"{attr}".ljust(max_len[idx], " "), end="")
        print("]")


# Print line
def print_line(size=20):
    print("+".ljust(size, "-"), "+")


# Main program
files = os.listdir("data")
for file in files:
    data = load_data("data/" + file)
    attributes = get_distinct_attr(data)
    histogram = count_occur(data)
    entropy = info(histogram[-1])
    decisions = count_occur_decision(data, attributes)
    total = len(data)
    attrs_entropy = info_attrs(decisions, attributes[0:-1], histogram[0:-1], total)
    info_gains = gain_attrs(entropy, attrs_entropy)

    # Print results
    padding = 36
    print_rows(data, 2, 20)
    print_line(padding)
    print(f"| {file}".ljust(padding, " "), "|")
    print_line(padding)
    print(f"| T = {entropy}".ljust(padding, " "), "|")
    print_line(padding)
    for idx, attr in enumerate(attributes[0:-1]):
        print(f"| Info(a{idx + 1}, T) = {attrs_entropy[idx]}".ljust(padding, " "), "|")
    print_line(padding)
    for idx, attr in enumerate(attributes[0:-1]):
        print(f"| Gain(a{idx + 1}, T) = {info_gains[idx]}".ljust(padding, " "), "|")
    print_line(padding)
    print("\n\n\n\n")
