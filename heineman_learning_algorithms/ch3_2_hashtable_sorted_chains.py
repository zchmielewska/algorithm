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


class HashtableLinked:
    """Separate chaining"""
    def __init__(self, m=10):
        self.table = [None] * m
        self.M = m
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


class HashtableLinkedSortedChains:
    """Separate chaining with sorted keys"""
    def __init__(self, m=10):
        self.table = [None] * m
        self.m = m
        self.n = 0

    def get(self, k):
        hc = hash(k) % self.m
        entry = self.table[hc]
        while entry:
            if entry.key > k:  # doesn't exist because keys are sorted
                return None
            if entry.key == k:
                return entry.value
            entry = entry.next
        return None

    def put(self, k, v):
        hc = hash(k) % self.m
        entry = self.table[hc]
        if entry is None:
            self.n += 1
            self.table[hc] = LinkedEntry(k, v, self.table[hc])
            return

        prev = None
        while entry:
            if entry.key > k:  # We can insert
                self.n += 1
                if prev is None:
                    self.table[hc] = LinkedEntry(k, v, entry)
                else:
                    prev.next = LinkedEntry(k, v, entry)
                return

            if entry.key == k:
                entry.value = v
                return

            prev, entry = entry, entry.next

        # Key is the largest
        prev.next = LinkedEntry(k,v)
        self.n += 1


if __name__ == "__main__":
    ht_sizes = [214_219, 524_287, 999_983]
    num_words = 160_564
    num_exer = 10**7

    for ht_size in ht_sizes:
        print("\nHashtable size:", ht_size)

        timing1 = timeit.timeit(
            stmt="""
for word in words:
    ht.get(word)
            """,
            setup=f"""
from ch3_2_hashtable_sorted_chains import english_words, HashtableOpen
words = english_words()
words = reversed(words[:{num_words}])
ht = HashtableOpen({ht_size})
for word in words:
    ht.put(word, word)
            """, number=num_exer)

        print("Timing for linear probing hashtable:", timing1)

        timing2 = timeit.timeit(
            stmt="""
for word in words:
    ht.get(word)
                """,
            setup=f"""
from ch3_2_hashtable_sorted_chains import english_words, HashtableLinked
words = english_words()
words = reversed(words[:{num_words}])
ht = HashtableLinked({ht_size})
for word in words:
    ht.put(word, word)
                """, number=num_exer)

        print("Timing for separate chaining hashtable:", timing2)

        timing3 = timeit.timeit(
            stmt="""
for word in words:
    ht.get(word)
                """,
            setup=f"""
from ch3_2_hashtable_sorted_chains import english_words, HashtableLinkedSortedChains
words = english_words()
words = reversed(words[:{num_words}])
ht = HashtableLinkedSortedChains({ht_size})
for word in words:
    ht.put(word, word)
                """, number=num_exer)

        print("Timing for separate chaining hashtable with sorted chains:", timing3)
