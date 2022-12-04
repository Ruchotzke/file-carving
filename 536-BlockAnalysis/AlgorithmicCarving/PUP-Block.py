"""
Name: PUP-Block.py
Author: Ethan Ruchotzke ethanr@iastate.edu
Purpose: A class to contain a basic PUP block.
"""


class PUPBlock:
    """
    A block containing data for assignment with PUP. Analogue for a block of file data.
    """

    def __init__(self, file, seq):
        """
        Initialize a new PUP block.
        :param file: The "file" identifier
        :param seq: The sequence number of the block inside the file
        """
        self.file = file
        self.seq = seq

    def get_distance(self, other):
        """
        Get the similarity distance between this block and another.
        :type other: PUPBlock
        :param other: The other block being compared to this one.
        :return: a numeric value representing the distance
        """
        if self.file == other.file:
            return abs(self.seq - other.seq)
        else:
            return abs(self.seq - other.seq) + 5  # extra offset to emulate a good comparison function
