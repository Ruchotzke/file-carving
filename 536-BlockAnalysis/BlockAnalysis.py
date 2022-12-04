"""
Name: BlockAnalysis.py
Author: Ethan Ruchotzke ethanr@iastate.edu
Purpose: A file used to test out some of the basic block size inference ideas with a main - final project, cpre536 f2022.
"""

# Open a binary file for testing
from BlockSizeInference.BlockSizeCalculator import BlockSizeCalculator

path = "./BlockSizeInference/blob.bin"

# create a handle
handle = open(path, 'rb')

# scan the file into an analysis object
analyzer = BlockSizeCalculator(handle)
handle.close()

print(len(analyzer.find_points_of_interest()))