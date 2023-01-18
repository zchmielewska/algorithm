import pandas as pd


def english_words():
    word_file = open("resource/words.english.txt", 'r')
    all_words = word_file.read().splitlines()
    word_file.close()
    return all_words


def base26(w):
    val = 0
    for ch in w.lower():
        next_digit = ord(ch) - ord("a")
        val = 26*val + next_digit
    return val


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


def get_stats(ht):
    size = len(ht.table)
    sizes = {}
    total_search = 0
    max_length = 0
    total_non_empty = 0
    for i in range(size):
        num = 0
        idx = i
        entry = ht.table[idx]
        total_non_empty += 1 if entry else 0

        while entry:
            entry = entry.next
            num += 1
            total_search += num

        if num in sizes:
            sizes[num] = sizes[num] + 1
        else:
            sizes[num] = 1

        if num > max_length:
            max_length = num

    if total_non_empty == 0:
        return 0, 0

    return ht.N/total_non_empty, max_length


def main():
    df = pd.DataFrame({"m": [], "avg": [], "max": [], "is_prime": []})
    words = english_words()

    lo = 428_880
    primes = [428_899, 428_951, 428_957, 428_977]
    hi = 428_980

    keys = [base26(w) for w in words]

    for m in range(lo, hi+1):
        print("m =", m)
        ht_linked = HashtableLinked(m)

        for k in keys:
            ht_linked.put(k, 1)

        avg_linked, max_linked = get_stats(ht_linked)
        is_prime = m in primes
        temp = pd.DataFrame({"m": [m], "avg": [avg_linked], "max": [max_linked], "is_prime": [is_prime]})
        df = pd.concat([df, temp], ignore_index=True)

    return df


if __name__ == "__main__":
    df = main()
