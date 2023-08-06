from wp.cache_get import CacheGet


# Abstract base for cache incr and cache decr.
class CacheDecrIncr(CacheGet):
    command = ['cache']

    # [<offset>]
    # The amount by which to decrement the item’s value.
    # ---
    # default: 1
    # ---
    offset = 1

    def __init__(self, key, **args):
        super().__init__(key, **args)

        self.offset = self.get_arg_value(key="offset", default_value=self.offset)

    def params(self):
        return [
            self.key,
            self.offset,
            self.group,
        ]

    def get_excluded_attrs(self):
        return super().get_excluded_attrs() + [
            "offset",
        ]
