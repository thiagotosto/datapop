import random
import string

class Utils():

    @staticmethod
    def generateKey(length):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
