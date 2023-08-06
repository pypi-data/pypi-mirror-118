from wp.command import WPCommand


# Gets a value from the object cache.
# Errors if the value doesn’t exist.
# wp cache get my_key my_group
class CacheGet(WPCommand):
    command = ['cache', 'get']

    # <key>
    # Cache key.
    key = ""

    # [<group>]
    # Method for grouping data within the cache which allows the same key to be used across groups.
    # ---
    # default: default
    # ---
    group = ""

    def __init__(self, key, **args):
        super().__init__(**args)

        self.key = key
        self.group = self.get_arg_value(key="group", default_value=self.group)

    def params(self):
        return [
            self.key,
            self.group,
        ]

    def get_excluded_attrs(self):
        return [
            "key",
            "group",
        ]
