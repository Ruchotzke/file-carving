"""
Name: BlockSizeCalculator.py
Author: Ethan Ruchotzke ethanr@iastate.edu
Purpose: A file used to test out some of the basic block size inference ideas - final project, cpre536 f2022.
"""
from HeaderAnalysis.SignatureAnalysis import SigReader


class BlockSizeCalculator:
    """
    A class used to help infer the size of blocks from a solid block of data.
    """

    def __init__(self, file_handle):
        """
        Construct a new BlockSizeCalculator.
        :param file_handle An active handle to a file object containing the binary object to be parsed.
        """
        self.binary_data = file_handle.read()

    def find_points_of_interest(self):
        """
        Find the points of interest for this object's binary data.
        Points of interest are defined as file headers (signatures).
        :return: A list of offsets where file signatures were found (bytes)
        """
        # save points of interest (indices / byte offsets)
        poi = []

        # create a signature analyzer
        reader = SigReader()

        # iterate over the entire dataset, byte by byte
        # check each part for a match with signatures
        # if a match was found, record the point of interest
        print("starting POI analysis. " + str(int(len(self.binary_data) / 100)) + " bytes to analyze.")
        for i in range(0, int(len(self.binary_data) / 100)):
            bytestring = self.binary_data[i:]
            if reader.check_signatures(bytestring) is not None:
                poi.append(i)
            if i % 10000 == 0:
                print("...... analyzed byte " + str(i))



        # return indices of the points of interest
        return poi
