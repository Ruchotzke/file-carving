import os
import random

from os import listdir
from os.path import isfile, join

# Parameter Variables
PULL_DIRECTORY = "./FilesToCombine"
PUSH_DIRECTORY = "./"
BLOCK_SIZE = 4096

# Generate a new binary file to write data into
output = open(PUSH_DIRECTORY + "/blob.bin", "wb")

# Generate a map for the generated data
output_map = open(PUSH_DIRECTORY + "/map.txt", "w")
output_map.write("Output Map for blob.bin\n\n")

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
    output_map.write(str(files[filename][0]) + '\n')
    output_map.write("%-50s   %-15d   %-15d\n" % (filename, lengths[filename], len(files[filename])))
output_map.write("\n")

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