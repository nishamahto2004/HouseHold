import hashlib

class Encryption:
    def convert(self,data):
        data = hashlib.sha256(data.encode())
        data = data.hexdigest()
        return data
