import os
import random

from os import listdir
from os.path import isfile, join

# Parameter Variables
PULL_DIRECTORY = "./DataGeneration/FilesToCombine"      # The directory to pull input files from
PUSH_DIRECTORY = "./DataGeneration/TestDataset"         # The directory to push output files to (including map)
BLOCK_SIZE = 4096                                       # The block size for the fragmentation
SEPARATE_BLOCKS = True                                  # Should blocks be saved into individual files, or one large file
RANDOMIZE_FRAGMENTS = True                              # Should the fragments always be in order, or can they be stored out of order
COHESIVENESS = 0                                        # How much should files be laid out together in one block (0 - random fragmentation, 1 - no fragmentation)

# Generate a map for the generated data
output_map = open(PUSH_DIRECTORY + "/_map.txt", "w")
output_map.write("Output Map for TestDataGenerator\n\n")

# Generate a new binary file to write data into if we are not separating blocks
if not SEPARATE_BLOCKS:
    output = open(PUSH_DIRECTORY + "/blob.bin", "wb")

# Read all files into memory for fragmentation
files = {}
lengths = {}
total_blocks = 0
for filename in [f for f in listdir(PULL_DIRECTORY) if isfile(join(PULL_DIRECTORY, f))]:
    file = open(PULL_DIRECTORY + "/" + filename, "rb")
    files[filename] = []
    file_length = 0

    # Read this file into chunks. Stop reading once we've hit slack space
    while True:
        next_block = file.read(BLOCK_SIZE)
        files[filename].append(next_block)
        total_blocks += 1
        file_length += len(next_block)
        if len(next_block) < BLOCK_SIZE:
            break

    # Save the length
    lengths[filename] = file_length

    # Close the file
    file.close()

# Calculate input size
total_input_size = 0
for key in lengths:
    total_input_size += lengths[key]

# Calculate the total output size, and update the map
output_map.write("%-25s %10d\n" % ("Input Size:", total_input_size))
output_map.write("%-25s %10d\n" % ("Output Size:", total_blocks * BLOCK_SIZE))
output_map.write("%-25s %10d\n" % ("Block Size:", BLOCK_SIZE))
output_map.write("%-25s %10d\n" % ("Total Blocks:", total_blocks))
output_map.write("\n")

# Write out the input file information into the map
output_map.write("%-50s   %-15s   %-15s\n" % ("FILENAME", "FILE SIZE", "TOTAL BLOCKS"))
for filename in files:
    # output_map.write(str(files[filename][0]) + '\n')
    output_map.write("%-50s   %-15d   %-15d\n" % (filename, lengths[filename], len(files[filename])))
output_map.write("\n")

if not SEPARATE_BLOCKS:
    # Add the header to the map for the block map
    output_map.write("%-12s  %-12s  %-50s  %-10s\n" % ("FILE OFFSET", "BLOCK OFFSET", "FILENAME", "FILE BLOCK"))

    # Fragmentation Helper Variables
    written_blocks = 0
    blocks_per_file = {}
    for filename in files:
        blocks_per_file[filename] = 0

    # Arrange and write fragmented blocks to the file
    while written_blocks < total_blocks:
        # Select the next block
        next_file = random.choice(list(files.keys()))

        # Remove the block from its container (it's been written)
        block = files[next_file].pop(0)

        # If we finished a file, we need to delete its file from memory and add slack space
        if len(files[next_file]) == 0:
            # Delete the file from memory
            del files[next_file]

            # Add slack space to the block (random garbage for now)
            block = b"".join([block, random.randbytes(BLOCK_SIZE - len(block))])

        # Write the block
        output.write(block)

        # Update the map
        output_map.write("%-12s  %12d  %-50s  %10d\n" % ("%#010x" % (written_blocks * BLOCK_SIZE), written_blocks, next_file, blocks_per_file[next_file]))

        # Update state variables
        written_blocks += 1
        blocks_per_file[next_file] += 1
else:
    # Add the header to the map for the block map
    output_map.write("%-12s  %-50s  %-10s\n" % ("FILE NUMBER", "FILENAME", "FILE BLOCK"))

    # We need to make a new file for each block with this option
    # Fragmentation variables
    written_blocks = 0
    blocks_per_file = {}
    for filename in files:
        blocks_per_file[filename] = 0

    # Iterate through each block
    while written_blocks < total_blocks:
        # Select the next block
        # Pick a random file and a random block
        next_file = random.choice(list(files.keys()))
        block_index = 0
        block = files[next_file].pop(block_index)

        # If we finished a file, we need to delete its file from memory and add slack space
        if len(files[next_file]) == 0:
            # Delete the file from memory
            del files[next_file]

            # Add slack space to the block (random garbage for now)
            block = b"".join([block, random.randbytes(BLOCK_SIZE - len(block))])

        # Write the block
        file = open(PUSH_DIRECTORY + "/BLOCK" + ("%05d" % written_blocks), "wb")
        file.write(block)
        file.close()

        # Update the map
        output_map.write("%-12s  %-50s  %-10s\n" % (("%05d" % written_blocks), next_file, str(blocks_per_file[next_file])))

        # Update state variables
        written_blocks += 1
        blocks_per_file[next_file] += 1

