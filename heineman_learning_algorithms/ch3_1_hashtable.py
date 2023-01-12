import timeit
import math


def english_words():
    word_file = open("resource/words.english.txt", 'r')
    all_words = word_file.read().splitlines()
    word_file.close()
    return all_words


class Entry:
    def __init__(self, k, v):
        self.key = k
        self.value = v


class LinkedEntry:
    def __init__(self, k, v, rest=None):
        self.key = k
        self.value = v
        self.next = rest


class HashtableOpen:
    """Open addressing"""
    def __init__(self, m=10):
        self.table = [None] * m
        self.m = m
        self.n = 0

    def get(self, k):
        hc = hash(k) % self.m
        while self.table[hc]:
            if self.table[hc].key == k:
                return self.table[hc].value
            hc = (hc + 1) % self.m
        return None

    def put(self, k, v):
        hc = hash(k) % self.m
        while self.table[hc]:
            if self.table[hc].key == k:
                self.table[hc].value = v
                return
            hc = (hc + 1) % self.m

        if self.n >= self.m - 1:
            raise RuntimeError("HashtableOpen is full.")

        self.table[hc] = Entry(k, v)
        self.n += 1


class HashtableTriangleNumbers:
    """Triangle probing"""

    def __init__(self, m=10):
        self.table = [None] * m

        exp = int(math.log2(m))
        if m != 2 ** exp:
            raise ValueError("The parameter 'm' must be a power of 2.")

        self.m = m
        self.n = 0

    def get(self, k):
        hc = hash(k) % self.m
        delta = 0
        idx = 0
        while self.table[hc]:
            idx += 1
            if self.table[hc].key == k:
                return self.table[hc].value
            delta += idx
            hc = (hc + delta) % self.m
        return None

    def put(self, k, v):
        hc = hash(k) % self.m
        delta = 0
        idx = 0
        while self.table[hc]:
            idx += 1
            if self.table[hc].key == k:
                self.table[hc].value = v
                return
            delta += idx
            hc = (hc + delta) % self.m

        if self.n >= self.m - 1:
            raise RuntimeError("HashtableOpen is full.")

        self.table[hc] = Entry(k, v)
        self.n += 1


class HashtableLinked:
    """Separate chaining"""
    def __init__(self, M=10):
        self.table = [None] * M
        self.M = M
        self.N = 0

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


if __name__ == "__main__":
    # ht_size = 524_288
    # num_words = 160_564

    ht_size = 64
    num_words = 21

    timing1 = timeit.timeit(
        stmt="""
for word in words:
    ht.get(word)
        """,
        setup=f"""
from ch3_1_hashtable import english_words, HashtableOpen
words = english_words()
words = words[:{num_words}]
ht = HashtableOpen({ht_size})
for word in words:
    ht.put(word, word)
        """)

    print("Timing for linear probing hashtable:", round(timing1, 2))

    timing2 = timeit.timeit(
        stmt="""
for word in words:
    ht.get(word)
            """,
        setup=f"""
from ch3_1_hashtable import english_words, HashtableTriangleNumbers
words = english_words()
words = words[:{num_words}]
ht = HashtableTriangleNumbers({ht_size})
for word in words:
    ht.put(word, word)
            """)

    print("Timing for triangular probing hashtable:", round(timing2, 2))

    timing3 = timeit.timeit(
        stmt="""
for word in words:
    ht.get(word)
            """,
        setup=f"""
from ch3_1_hashtable import english_words, HashtableLinked
words = english_words()
words = words[:{num_words}]
ht = HashtableLinked({ht_size})
for word in words:
    ht.put(word, word)
            """)

    print("Timing for separate chaining hashtable:", round(timing3, 2))
