import json
from HeaderAnalysis.signature_object import SignatureObject

# BEWARE: ZIP TRAILER HAS BEEN ALTERED. DOUBLE CHECK IT


class SigReader:
    def __init__(self):
        """
        Generate a signature reader object.
        """
        # Load the signature PDF_Data into memory
        sig_file = open("./Carving/file_sigs.json", "r")
        sig_dict = json.load(sig_file)
        sig_file.close()

        # Parse signatures into useful objects
        # ELIMINATE ANY SIGNATURES OF 1 BYTE OR LESS
        self.signatures = []
        for entry in sig_dict["filesigs"]:
            if len(bytes.fromhex(entry['Header (hex)'])) >= 2:
                self.signatures.append(
                    SignatureObject(entry['Header (hex)'], entry['Trailer (hex)'], entry['Header offset'],
                                    entry['File extension'], entry['File description'], entry['FileClass']))

    def check_signatures(self, byte_data: bytes):
        """
        Check the signatures database against byte PDF_Data. Only checks the initial portion
        of the byte PDF_Data for a signature.
        :param byte_data: The byte PDF_Data to be analyzed
        :return: the signature object which matches the file
        """
        for signature in self.signatures:
            if byte_data.startswith(signature.header):
                return signature

        return None
