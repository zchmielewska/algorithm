def english_words():
    word_file = open("resource/words.english.txt", 'r')
    all_words = word_file.read().splitlines()
    word_file.close()
    return all_words


class ValueBadHash:
    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return hash(self.v) % 4

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.v == other.v


class LinkedEntry:
    def __init__(self, k, v, rest=None):
        self.key = k
        self.value = v
        self.next = rest


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


def main(size=10):
    good_ht = HashtableLinked(size)
    bad_ht = HashtableLinked(size)
    words = english_words()[:5000]

    for w in words:
        good_ht.put(w, True)
        bad_ht.put(ValueBadHash(w), True)

    good = get_stats(good_ht)
    bad = get_stats(bad_ht)
    result = f"good: {good}, bad: {bad}"
    return result


if __name__ == "__main__":
    result = main(50000)
    print(result)
