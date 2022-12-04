"""
Name: CharacterizationTester.py
Author: Ethan Ruchotzke ethanr@iastate.edu
Purpose: To test characterizations of PDFs and JPGs on their test set
"""
import os
import numpy as np
from matplotlib import pyplot as plt

from FragmentSorting.CharacterizationConstants import *
from FragmentSorting.Statistics import StatisticsCounter
from scipy.spatial import distance

# Parameters
NUM_PDF = 10         # How many PDF should be tested
NUM_JPG = 1000        # How many JPG should be tested

def ngram_characterize(bytestring, n):
    """
    Generate a characterization mapping (ngram value to count of ngrams) for a given
    set of bytes.
    :param bytestring: The PDF_Data to be characterized
    :param n: The size of the ngrams
    :return: An array containing the count of each byte value in this bytestring
    """
    # Generate an array for output, effective a histogram of shingles
    arr = np.zeros((2 ** (8 * n)))  # need to potentially allocate more room if we increase n (n can likely only go to 2)

    # Iterate through each ngram and count it
    for i in range(0, len(bytestring) - n + 1):
        ngram = bytestring[i:i + n]
        ngram = int.from_bytes(ngram, 'big')
        arr[ngram] += 1

    # Normalize the characterization by the number of ngrams read
    for i in range(0, len(arr)):
        arr[i] /= len(bytestring) - n + 1

    # Return the characterization
    return arr


def file_characterize(file_handle, ngram_size, block_size=512):
    """
    Generate a characterization of the file, block by block.
    :param file_handle: The open file to characterize
    :param ngram_size: The size of shingle to be used for characterization (bytes)
    :param block_size: The block size to chunk by, defaults to 512
    :return: A list of dictionaries with block characterizations (ordered first to last)
    """
    # Create an array for output
    out = []

    # Parse the file, block by block
    while True:
        chunk = file_handle.read(block_size)

        # if EOF, none will be returned from the read
        if not chunk:
            # EOF
            break

        # Characterize this block
        character = ngram_characterize(chunk, ngram_size)

        # Store this characterization
        out.append(character)

    # Return the file characterization
    return out

# Load the characterization data
pdf_mean = np.load(CHARACTERIZATION_DIRECTORY + "pdf-mean.npy")
pdf_cov = np.load(CHARACTERIZATION_DIRECTORY + "pdf-cov.npy")
jpg_mean = np.load(CHARACTERIZATION_DIRECTORY + "jpg-mean.npy")
jpg_cov = np.load(CHARACTERIZATION_DIRECTORY + "jpg-cov.npy")

# Load the filenames of the two test sets we can use
pdf_test_set = os.listdir(PDF_DIRECTORY)
pdf_test_set = pdf_test_set[int(TRAINING_TESTING_PERCENT * len(pdf_test_set)):]
jpg_test_set = os.listdir(JPG_DIRECTORY)
jpg_test_set = jpg_test_set[int(TRAINING_TESTING_PERCENT * len(jpg_test_set)):]

# Create a test set along with classifications
test_set = []
for i in range(0, NUM_PDF):
    with open(PDF_DIRECTORY + pdf_test_set[i], "rb") as pdf:
        character = file_characterize(pdf, ngram_size=1, block_size=BLOCK_SIZE)
        for block in character:
            test_set.append(("pdf", block))

for i in range(0, NUM_JPG):
    with open(JPG_DIRECTORY + jpg_test_set[i], "rb") as jpg:
        character = file_characterize(jpg, ngram_size=1, block_size=BLOCK_SIZE)
        for block in character:
            test_set.append(("jpg", block))

jpg_count = 0
pdf_count = 0
for entry in test_set:
    if entry[0] == "jpg":
        jpg_count += 1
    else:
        pdf_count += 1

print("pdf: " + str(pdf_count) + " jpg: " + str(jpg_count))

# Perform a validation test using cosine distance
true_pdf = StatisticsCounter()
false_pdf = StatisticsCounter()
true_jpg = StatisticsCounter()
false_jpg = StatisticsCounter()
for sample in test_set:
    # Calculate cosine distance from both pdf and jpg
    pdf_dist = distance.euclidean(sample[1], pdf_mean)
    jpg_dist = distance.euclidean(sample[1], jpg_mean)

    if sample[0] == "pdf":
        true_pdf.add_sample(pdf_dist)
        false_jpg.add_sample(jpg_dist)
    else:
        true_jpg.add_sample(jpg_dist)
        false_pdf.add_sample(pdf_dist)

print("true PDF: " + str(true_pdf))
print("false PDF: " + str(false_pdf))
print("true JPG: " + str(true_jpg))
print("false JPG: " + str(false_jpg))

fig, axs = plt.subplots(4, sharex=True)
fig.suptitle("Euclidean Distance Histograms")
axs[0].title.set_text("True PDF")
axs[0].hist(np.array(true_pdf.values), bins=150)
axs[1].title.set_text("False PDF")
axs[1].hist(np.array(false_pdf.values), bins=150)
axs[2].title.set_text("True JPG")
axs[2].hist(np.array(true_jpg.values), bins=150)
axs[3].title.set_text("False JPG")
axs[3].hist(np.array(false_jpg.values), bins=150)
plt.show()