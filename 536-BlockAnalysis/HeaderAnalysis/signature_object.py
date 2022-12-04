class SignatureObject:
    def __init__(self, header, trailer, offset, extension , description, file_class):
        # Easy fields
        self.extension = extension
        self.description = description
        self.file_class = file_class

        # Offset is just decimal
        self.offset = int(offset)

        # Header and trailer are byte strings
        self.header = bytes.fromhex(header)
        if "null" in trailer:
            self.trailer = b''
        else:
            self.trailer = bytes.fromhex(trailer)

