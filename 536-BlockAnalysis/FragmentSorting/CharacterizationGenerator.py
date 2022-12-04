"""
Name: CharacterizationGenerator.py
Author: Ethan Ruchotzke ethanr@iastate.edu
Purpose: To create characterizations of both JPEG and PDF fragments and save them.
"""
import os

# Parameters
import numpy as np
from FragmentSorting.CharacterizationConstants import *


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


# PDF Characterization
# For each PDF, break it into blocks, and characterize blocks
# Characterization Data = mean, covariance matrix (for variance and covariance)

# Figure out the files to characterize for training
pdf_filenames = os.listdir(PDF_DIRECTORY)
training_files = pdf_filenames[:int(TRAINING_TESTING_PERCENT * len(pdf_filenames))]
print("Using " + str(len(training_files)) + " pdf files for characterization.")

# Create a container to save sample data
characterization_data = []

# Compute total data
i = 0
for filename in training_files:
    # Open each PDF file
    with open(PDF_DIRECTORY + filename, 'rb') as pdf:
        # Read each file block by block and generate a series of ngram distributions
        out = file_characterize(pdf, ngram_size=1, block_size=BLOCK_SIZE)

        # Save the data to the characterization data
        characterization_data += out

    i += 1
    if i % 100 == 0:
        print("Processed file " + str(i))

# Combine all pdf data into a mean and covariance matrix for characterization
print("Characterizing blocks...")
stacked = np.array(characterization_data).T  # the 2D version of the array used for numpy/scipy calc
print(stacked.shape)
mean = np.mean(stacked, axis=1)  # the mean of the distribution (centroid)
cov = np.cov(stacked)  # the covariance matrix of the distribution (for variance measurement)

# Save the characterization data to a file(s)
np.save(CHARACTERIZATION_DIRECTORY + "pdf-mean", mean)
np.save(CHARACTERIZATION_DIRECTORY + "pdf-cov", cov)
print("PDF Characterization saved")


# JPG Characterization
# For each JPG, break it into blocks, and characterize blocks
# Characterization Data = mean, covariance matrix (for variance and covariance)

# Figure out the files to characterize for training
jpg_filenames = os.listdir(JPG_DIRECTORY)
training_files = jpg_filenames[:int(TRAINING_TESTING_PERCENT * len(jpg_filenames))]
print("Using " + str(len(training_files)) + " jpg files for characterization.")

# Create a container to save sample data
characterization_data = []

# Compute total data
i = 0
for filename in training_files:
    # Open each PDF file
    with open(JPG_DIRECTORY + filename, 'rb') as jpg:
        # Read each file block by block and generate a series of ngram distributions
        out = file_characterize(jpg, ngram_size=1, block_size=BLOCK_SIZE)

        # Save the data to the characterization data
        characterization_data += out

    i += 1
    if i % 100 == 0:
        print("Processed file " + str(i))

# Combine all pdf data into a mean and covariance matrix for characterization
print("Characterizing blocks...")
stacked = np.array(characterization_data).T  # the 2D version of the array used for numpy/scipy calc
print(stacked.shape)
mean = np.mean(stacked, axis=1)  # the mean of the distribution (centroid)
cov = np.cov(stacked)  # the covariance matrix of the distribution (for variance measurement)

# Save the characterization data to a file(s)
np.save(CHARACTERIZATION_DIRECTORY + "jpg-mean", mean)
np.save(CHARACTERIZATION_DIRECTORY + "jpg-cov", cov)
print("JPG Characterization saved")
