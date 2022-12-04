from Carving.Block import Block
import os

from HeaderAnalysis.SignatureAnalysis import SigReader


def pup(blocks):
    """
    Apply the PUP (parallel unique paths) algorithm to the supplied block
    list to generate several potential files for recovery.
    :param blocks: The blocks to be analyzed / reconstructed.
    :return: Several potential files for recovery.
    """
    return None


def generate_blocks(path, signature_object: SigReader):
    """
    From a supplied filepath, generate a list of block
    objects.
    :param signature_object: the signature object for parsing signatures
    :param path: The path to the actual block files.
    :return: A list of block objects, named accordingly with the input files.
    """
    # Create a list for blocks
    blocklist = []

    # Open each file in the directory
    for filename in os.listdir(path):
        # Get the PDF_Data from the file
        file = open(path + "/" + filename, 'rb')
        data = file.read()
        file.close()

        # Generate a block object
        block = Block(filename, data)

        # Scan for a signature
        block.check_signatures(signature_object)

        # Add the block to a list
        blocklist.append(block)

    # Return the completed list
    return blocklist
