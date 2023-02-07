class RankBinaryNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.N = 1
        self.height = 0

    def contains(self, target):
        if target == self.key:
            return True

        if target < self.key:
            if self.left is None:
                return False
            return self.left.contains(target)

        if self.right is None:
            return False

        return self.right.contains(target)


class RankBinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return RankBinaryNode(key)

        if key <= node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.N = 1
        ht = -1

        if node.left:
            node.N += node.left.N
            ht = max(ht, node.left.height)
        if node.right:
            node.N += node.right.N
            ht = max(ht, node.right.height)
        node.height = ht + 1
        return node

    def _count(self, node):
        return 0 if node is None else node.N

    def select(self, k):
        return self._select(self.root, k)

    def _select(self, node, k):
        if node is None:
            return None
        leftN = self._count(node.left)

        if leftN > k:
            return self._select(node.left, k)
        if leftN < k:
            return self._select(node.right, k - leftN - 1)
        return node.key

    def rank(self, key):
        return self._rank(self.root, key)

    def _rank(self, node, key):
        if node is None:
            return 0

        if key == node.key:
            return self._count(node.left)
        if key < node.key:
            return self._rank(node.left, key)
        return 1 + self._count(node.left) + self._rank(node.right, key)

    def __contains__(self, target):
        if self.root is None:
            return False
        return self.root.contains(target)

