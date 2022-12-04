"""
Name: BlockSorter.py
Author: Ethan Ruchotzke ethanr@iastate.edu
Purpose: To use knowledge from the other files to characterize input blocks into 3 sets - PDF, JPG, and DOC
"""
import os
import numpy as np
from matplotlib import pyplot as plt

from FragmentSorting.CharacterizationConstants import *
from FragmentSorting.Statistics import StatisticsCounter
from scipy.spatial import distance

# Parameters
BLOCK_DIRECTORY = "../input-blockset/"
SORTED_DIRECTORY = "../sorted-blockset/"
DOC_DIR = "doc/"
JPG_DIR = "jpg/"
PDF_DIR = "pdf/"

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

# ALGORITHM
# Reach each block into memory
# Characterize the block read with 1-grams
# Calculate the distance to both a JPG and a PDF
# Sort based on cosine distance

# Cutoff distances for classification (found through trial and error)
pdf_cutoff = 0.27
jpg_cutoff = 0.17

# Counts
pdf_count = 0
jpg_count = 0
doc_count = 0

# Sort
for file in os.listdir(BLOCK_DIRECTORY):
    with open(BLOCK_DIRECTORY + file, "rb") as block:
        # Characterize the file
        data = block.read()
        character = ngram_characterize(data, n=1)
        character = np.array(character)  # turn into numpy array for distance

        # Calculate the cosine distance to both PDF and JPG
        pdf_dist = distance.euclidean(character, pdf_mean)
        jpg_dist = distance.euclidean(character, jpg_mean)

        # Classify the block based on distances
        is_pdf = pdf_dist <= pdf_cutoff
        is_jpg = jpg_dist <= jpg_cutoff
        if is_pdf and is_jpg:  # If both classifiers were active, pick the lower distance one
            if jpg_dist < pdf_dist:
                is_pdf = False
            else:
                is_jpg = False

        if is_pdf:  # Classified as PDF
            pdf_count += 1
            with open(SORTED_DIRECTORY + PDF_DIR + file, "wb") as copy:     # copy the data to the new dir
                copy.write(data)
        elif is_jpg:  # Classified as JPG
            jpg_count += 1
            with open(SORTED_DIRECTORY + JPG_DIR + file, "wb") as copy:     # copy the data to the new dir
                copy.write(data)
        else:  # Classified as DOC (or something else)
            doc_count += 1
            with open(SORTED_DIRECTORY + DOC_DIR + file, "wb") as copy:     # copy the data to the new dir
                copy.write(data)


# Print out some output
print("Classification done.")
print("Doc Blocks: " + str(doc_count))
print("PDF Blocks: " + str(pdf_count))
print("JPG Blocks: " + str(jpg_count))