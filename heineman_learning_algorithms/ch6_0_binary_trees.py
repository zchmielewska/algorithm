class Node:
    def __init__(self, val, rest=None):
        self.value = val
        self.next = rest


def sum_iterative(n):
    total = 0
    while n:
        total += n.value
        n = n.next
    return total


def sum_list(n):
    if n is None:
        return 0
    return n.value + sum_list(n.next)


class BinaryNode:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None
        self.height = 0

    def height_difference(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        return left_height - right_height

    def compute_height(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        self.height = 1 + max(left_height, right_height)


class BinaryTree:
    def __init__(self):
        self.root = None

    def __contains__(self, target):
        node = self.root
        while node:
            if target == node.value:
                return True

            if target < node.value:
                node = node.left
            else:
                node = node.right

        return False

    def __iter__(self):
        for v in self._inorder(self.root):
            yield v

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if node is None:
            return BinaryNode(val)

        if val <= node.value:
            node.left = self._insert(node.left, val)
        else:
            node.right = self._insert(node.right, val)
        return node

    def _remove_min(self, node):
        if node.left is None:
            return node.right

        node.left = self._remove_min(node.left)
        return node

    def remove(self, val):
        self.root = self._remove(self.root, val)

    def _remove(self, node, val):
        if node is None:
            return None

        if val < node.value:
            node.left = self._remove(node.left, val)
        elif val > node.value:
            node.right = self._remove(node.right, val)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            original = node
            node = node.right
            while node.left:
                node = node.left

            node.right = self._remove_min(original.right)
            node.left = original.left

        return node

    def _inorder(self, node):
        if node is None:
            return

        for v in self._inorder(node.left):
            yield v

        yield node.value

        for v in self._inorder(node.right):
            yield v
