import random


class Hash:
    arr = []

    def __init__(self, n: int):
        """
        Creates a hash table that hashes from integers in {0, ..., n -1} to {0,...,n-1}
        :param n: Size of Hash Table
        """
        arr = [i for i in range(n)]
        random.shuffle(arr)

    def hash(self, index: int) -> int:
        """
        :param index:
        :return: Returns a unique hash for index
        """
        return self.arr[index]
