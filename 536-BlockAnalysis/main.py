import hashlib


def shingle(msg):
    """
    Calculate the shingled version (bi-gram) of the input.
    :param msg: The message to be shingled
    :return: A shingled array of strings
    """
    # split the string into shingles of 2 parts (TO ADJUST)
    out_set = set()
    for i in range(0, len(msg) - 1):
        out_set.add("" + msg[i] + msg[i + 1])

    # return the shingles
    return out_set


def shingle_bytes(msg, shingle_size=2):
    """
    Calculate the bi-gram shingled version of the input.
    :param shingle_size: How many elements should be combined into a shingle
    :param msg: The bytes to be shingled
    :return: An output set of byte pairs
    """
    # split the input into shingles of 2 parts (TO ADJUST)
    out_set = set()
    for i in range(0, len(msg) - shingle_size - 1):
        arr = bytearray()
        for s in range(0, shingle_size):
            arr.append(msg[i + s])
        out_set.add(bytes(arr))

    # return the shingles
    return out_set


def simhash(shingles):
    """
    Calculate the simhash for a given shingled input.
    Based on https://matpalm.com/resemblance/simhash/
    :param shingles:The shingled input.
    :return: a 4 byte simhash bytes object
    """

    # Create an array to hold integers while calculating
    arr = [0] * 32
    for shingle in shingles:
        # Generate a hash
        shingle_hash = hashlib.shake_128(shingle).digest(4)

        # Iterate through the hash bit by bit
        # If the bit is set, add one to the arr, else sub from the corresponding index
        # Shifting to the right allows us to grab the rightmost bit
        for byte in range(0, 3):
            curr = shingle_hash[byte]
            for bit in range(0, 8):
                index = 8 * byte + (7 - bit)  # calculate the index into the arr, as its reversed
                arr[index] += 1 if (curr >> bit & 1) else -1

    # Generate an output based on the array value (4 byte hash)
    out_hash = bytearray(4)
    for byte in range(0, 3):
        for bit in range(0, 7):
            val = arr[8 * byte + (7 - bit)]
            if val > 0:
                out_hash[byte] = out_hash[byte] | (1 << bit)  # set the appropriate bit
    return bytes(out_hash)


def hamming_distance(in1, in2):
    """
    Calculate the hamming distance (difference between individual bits) for two bytestrings.
    :param in1: Bytestring 1
    :param in2: Bytestring 2
    :return: The hamming distance of the two inputs
    """

    # First ensure the two byte strings are identical lengths
    if len(in1) != len(in2):
        raise Exception("Input lengths for hamming distance must be identical.")

    # Iterate bit by bit, incrementing if the bits are not equivalent
    dist = 0
    for i in range(0, 8 * len(in1)):
        if (in1[int(i / 8)] >> (i % 8) & 1) != (in2[int(i / 8)] >> (i % 8) & 1):
            dist += 1

    # Return the hamming distance
    return dist


def compare_strings(msg1, msg2):
    """
    Compare two strings using the shingle, simhash, and hamming distance method.
    :param msg1:
    :param msg2:
    :return:
    """
    return hamming_distance(simhash(shingle(msg1)), simhash(shingle(msg2)))


def compare_bytes(msg1, msg2):
    """
    Compare two bytestrings using the shingle, simhash, and hamming distance method.
    :param msg1:
    :param msg2:
    :return:
    """
    return hamming_distance(simhash(shingle_bytes(msg1)), simhash(shingle_bytes(msg2)))

# Generate shingled inputs
print(compare_bytes(b'and the pl', b'ace was far away.'))
print(compare_bytes(b'and the place ', b'was far away.'))
print(compare_bytes(b'and the place was far away.', b' New thought. Here\'s some extra'))