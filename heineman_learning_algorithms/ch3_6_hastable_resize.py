import pandas as pd
import time


def english_words():
    word_file = open("resource/words.english.txt", 'r')
    all_words = word_file.read().splitlines()
    word_file.close()
    return all_words


class CountableHash:
    hash_count = 0

    def __init__(self, w):
        self.word = w

    def __hash__(self):
        CountableHash.hash_count += 1
        return hash(self.word)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.word == other.word


class LinkedEntry:
    def __init__(self, k, v, rest=None):
        self.key = k
        self.value = v
        self.next = rest


class DynamicHashtable:
    def __init__(self, M=10):
        if M < 1:
            raise ValueError("Storage must be at least 1.")

        self.table = [None] * M
        self.M = M
        self.N = 0
        self.load_factor = 0.75
        self.threshold = min(M * self.load_factor, M-1)

    def get(self, k):
        hc = hash(k) % self.M
        entry = self.table[hc]
        while entry:
            if entry.key == k:
                return entry.value
            entry = entry.next
        return None

    def put(self, k, v):
        hc = hash(k) % self.M
        entry = self.table[hc]
        while entry:
            if entry.key == k:
                entry.value = v
                return
            entry = entry.next

        self.table[hc] = LinkedEntry(k, v, self.table[hc])
        self.N += 1

        if self.N >= self.threshold:
            self.resize(2*self.M + 1)

    def resize(self, new_size):
        temp = DynamicHashtable(new_size)
        for n in self.table:
            while n:
                temp.put(n.key, n.value)
                n = n.next
        self.table = temp.table
        temp.table = None
        self.M = temp.M
        self.threshold = self.load_factor * self.M

    def remove(self, k):
        hc = hash(k) % self.M
        entry = self.table[hc]
        prev = None
        while entry:
            if entry.key == k:
                if prev:
                    prev.next = entry.next
                else:
                    self.table[hc] = entry.next
                self.N -= 1
                return entry.value

            prev, entry = entry, entry.next
        return None

    def __iter__(self):
        for entry in self.table:
            while entry:
                yield entry.key, entry.value
                entry = entry.next


def main():
    words = english_words()
    ht_dynamic = DynamicHashtable(1023)
    max_cost = 0
    ct = 0
    for w in words:
        start = time.time()
        ht_dynamic.put(CountableHash(w), w)
        end = time.time()
        cost = end - start
        if cost > max_cost:
            max_cost = cost
            print(f"{ct}: {end-start}")
        ct += 1


if __name__ == "__main__":
    main()
