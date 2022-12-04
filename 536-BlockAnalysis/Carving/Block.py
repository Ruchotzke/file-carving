from HeaderAnalysis.SignatureAnalysis import SigReader


class Block:
    """
    A block is an in-memory abstraction of a block of PDF_Data to be reconstructed.
    """
    def __init__(self, name, data):
        """
        Initialize the block.
        :param name: The name of the block (identifier, typically a number)
        :param data: The PDF_Data contained in the block.
        """
        self.name = name
        self.data = data

        # Does this block contain a signature?
        self.signature = None

    def check_signatures(self, sig_object: SigReader):
        """
        Check the block for any signature objects.
        :param sig_object: The signature object containing a SigReader to analyze bytes with.
        :return: Nothing
        """
        self.signature = sig_object.check_signatures(self.data)
