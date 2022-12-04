"""
A file used to calculate ngram values for the chunks in a common document.
Plan of action: build ngram sets from PDF and JPEG sets (all other blocks will belong to the word document).
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance


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


# Generate a characterization of the file
file = open("CharacterizationData/PDF_Data/2A2C2V4WI5YRDJHR26XUD4IAULIYGTMA.pdf", "rb")
out = file_characterize(file, 1)
file.close()

# Calculate Mahalanobis distance from the PDF samples
stacked = np.array(out).T           # the 2D version of the array used for numpy/scipy calc
mean = np.mean(stacked, axis=1)     # the mean of the distribution (centroid)
cov = np.cov(stacked)               # the covariance matrix of the distribution (for distance measurement)
inverse = np.linalg.inv(cov)        # the inverse of the covariance matrix (used for Mahalanobis)

# Print some distances
test_point = np.random.rand(256)
for i in range(0, 256):
    test_point[i] = int(2 * test_point[i])
print("random = " + str(distance.cosine(mean, test_point)))

test_point = out[0]
print(distance.cosine(mean, test_point))
test_point = out[1]
print(distance.cosine(test_point, mean))
test_point = out[2]
print(distance.cosine(test_point, mean))
test_point = out[3]
print(distance.cosine(test_point, mean))
test_point = out[4]
print(distance.cosine(test_point, mean))
test_point = out[5]
print(distance.cosine(test_point, mean))
test_point = out[6]
print(distance.cosine(test_point, mean))
test_point = out[7]
print(distance.cosine(test_point, mean))
test_point = out[8]
print(distance.cosine(test_point, mean))
test_point = out[9]
print(distance.cosine(test_point, mean))

# # Print some distances
# test_point = out[0]
# print(distance.mahalanobis(mean, test_point, inverse))
# test_point = out[1]
# print(distance.mahalanobis(test_point, mean, inverse))
# test_point = out[2]
# print(distance.mahalanobis(test_point, mean, inverse))
# test_point = out[3]
# print(distance.mahalanobis(test_point, mean, inverse))
# test_point = out[4]
# print(distance.mahalanobis(test_point, mean, inverse))
# test_point = out[5]
# print(distance.mahalanobis(test_point, mean, inverse))
# test_point = out[6]
# print(distance.mahalanobis(test_point, mean, inverse))
# test_point = out[7]
# print(distance.mahalanobis(test_point, mean, inverse))
# test_point = out[8]
# print(distance.mahalanobis(test_point, mean, inverse))
# test_point = out[9]
# print(distance.mahalanobis(test_point, mean, inverse))

# # Graph the file characterization
# for char in range(3, 6):
#     character = out[char]
#     x_axis = []
#     y_axis = []
#     for i in range(0, 256):
#         x_axis.append(i)
#         y_axis.append(character[i] if i in character else 0)
#     plt.plot(x_axis, y_axis)
#
#
# plt.title('title name')
# plt.xlabel('x_axis name')
# plt.ylabel('y_axis name')
# plt.show()
