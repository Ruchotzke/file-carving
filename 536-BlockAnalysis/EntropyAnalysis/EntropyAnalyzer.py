import math
import os


def calculate_entropy(data: bytes):
    # First create a count of each independent value
    mapping = {}
    for byte in data:
        if byte in mapping:
            mapping[byte] += 1
        else:
            mapping[byte] = 1

    # Turn the counts into probabilities
    for entry in mapping:
        mapping[entry] /= len(data)

    # Calculate shannon entropy
    sum = 0
    for entry in mapping:
        sum += mapping[entry] * math.log2(1 / mapping[entry])

    # Return the result
    return sum


string = b"hello there in bytes"
print(calculate_entropy(string))
string = b"aaaaaaaaaaaaaaaaaaaaaaaaaaaa"
print(calculate_entropy(string))
string = b"sakjfdhasiuf20837ldsfsd jhfkasfa98sf8ysa9f"
print(calculate_entropy(string))