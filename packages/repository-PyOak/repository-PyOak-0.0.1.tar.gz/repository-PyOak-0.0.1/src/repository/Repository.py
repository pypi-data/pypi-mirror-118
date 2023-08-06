from collections import OrderedDict

class Repository(dict):

    def __init__(self, items: dict = {}):
        """Create a new repository."""

        # All of the respository items
        self._items = OrderedDict(items)

    def has(self, key):
        """Determine if the given configuration value exists."""

        return key in self._items
    
    def get(self, key, default = None):
        """Get the specified value from the repository, or a default value."""

        if type(key) is list:
            raise NotImplementedError
        
        return self._items.get(key, default)

    def set(self, key, value = None):
        """Set a given key in the repository."""

        keys = {}

        if not type(key) is dict:
            keys.update({key: value})
        
        self._items.update(keys)

    def prepend(self, key, value):
        """Prepend a value onto an list repository value."""

        items = self.get(key)

        items.insert(0, value)

        self.set(key, items)

    def append(self, key, value):
        """Append a value onto an list repository value."""

        items = self.get(key)

        items.append(value)

        self.set(key, items)

    def remove(self, key):
        """Remove the given key from the repository."""
        del self._items[key]

    def all(self):
        return self._items

    def keys(self):
        return self._items.keys()

    def items(self):
        return self._items.items()

    def values(self):
        return self._items.values()

    def __len__(self):
        return len(self._items)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        del self._items[key]

    def __missing__(self, key):
        raise KeyError(key)
    
    def __iter__(self):
        return iter(self._items)

    def __reversed__(self):
        return OrderedDict(reversed(list(self._items.items())))

    def __contains__(self, key):
        return key in self._items
