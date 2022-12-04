import math
import random

SAMPLE_COUNT = 500
GENERATION_PERIOD = 5
GENERATION_ERROR = 0.00
SAMPLES_TO_REMOVE = 50

CLUSTERING_MIN = 2
CLUSTERING_MAX = 30
CLUSTERING_STEP = 1

# Generate a dataset for testing
data = [0.0]
for i in range(1, SAMPLE_COUNT + SAMPLES_TO_REMOVE):
    data.append(data[i-1] + GENERATION_PERIOD * (1.0 - (random.random() - 0.5) * 2 * GENERATION_ERROR))

# Remove some samples to make it incomplete
for i in range(0, SAMPLES_TO_REMOVE):
    data.pop(random.randrange(0, len(data)))

# Clustering Analysis
for p in range(CLUSTERING_MIN, CLUSTERING_MAX, CLUSTERING_STEP):
    # Generate a recurrent sample of the initial data
    sample = [i % p for i in data]

    # Normalize the sample to [0,1] to check clustering
    high_range = max(sample)
    if high_range == 0:
        high_range = 1 # No impact on clustering if they are all at timestamp 0

    sample = [i / high_range for i in sample]

    # Calculate the variance, starting with mean
    mean = 0
    for item in sample:
        mean += item
    mean /= len(sample)

    # Calculate the variance
    s2 = 0
    for item in sample:
        s2 += (item - mean) * (item - mean)
    s2 /= len(sample) - 1

    # Standard deviation
    s = math.sqrt(s2)
    print("Period " + str(p) + " has stddev " + str(s))