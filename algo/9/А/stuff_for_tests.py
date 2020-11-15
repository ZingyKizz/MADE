class FakeCartesianTree:
    """Фейковое дерево поиска"""
    def __init__(self):
        self.tree = set()

    def insert(self, val):
        self.tree.add(val)

    def delete(self, val):
        self.tree.discard(val)

    def exists(self, val):
        res = "true" if val in self.tree else "false"
        return res

    def next(self, val):
        keys = list(self.tree)
        keys.sort()
        for i in keys:
            if i > val:
                return i
        return "none"

    def prev(self, val):
        keys = list(self.tree)
        keys.sort(reverse=True)
        for i in keys:
            if i < val:
                return i
        return "none"
