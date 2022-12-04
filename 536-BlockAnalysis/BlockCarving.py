# Parameters
from Carving.PUP import generate_blocks
from HeaderAnalysis.SignatureAnalysis import SigReader

path = "input-blockset"

# Generate a signature object
sig_reader = SigReader()

# Generate a blocklist
blocks = generate_blocks(path, sig_reader)
for block in blocks:
    # If the block is ascii, ignore it
    # is_ascii = True
    # try:
    #     block.PDF_Data.decode('ascii')
    # except:
    #     is_ascii = False
    #
    # if is_ascii:
    #     continue

    # Check the extension
    if block.signature is not None:
        print(str(block.signature.extension) + " " + str(block.signature.header) + " " + str(len(block.signature.header)))
