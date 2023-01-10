import timeit


def english_words():
    word_file = open("resource/words.english.txt", 'r')
    all_words = word_file.read().splitlines()
    word_file.close()
    return all_words


class Entry:
    def __init__(self, k, v):
        self.key = k
        self.value = v


class Hashtable:
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
            raise RuntimeError("Hashtable is full.")

        self.table[hc] = Entry(k, v)
        self.n += 1


if __name__ == "__main__":
    timing = timeit.timeit(
        stmt="""
    for word in words:
        ht.get(word)
        """,
        setup="""
    from ch3_1_hashtable import english_words, Hashtable
    words = english_words()[:15]
    ht = Hashtable(45)
    for word in words:
        ht.put(word, word)
        """)

    print(timing)
