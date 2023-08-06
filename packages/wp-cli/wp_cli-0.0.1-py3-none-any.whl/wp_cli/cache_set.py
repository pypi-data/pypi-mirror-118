from wp.cache_get import CacheGet


# TODO Test.
# Sets a value to the object cache, regardless of whether it already exists.
# Errors if the value can’t be set.
# wp cache set my_key my_value my_group 300
# Success: Set object 'my_key' in group 'my_group'.
class CacheSet(CacheGet):
    command = ['cache', "set"]

    # <value>
    # Value to add to the key.
    value = ""

    # [<expiration>]
    # Define how long to keep the value, in seconds. 0 means as long as possible.
    # ---
    # default: 0
    # ---
    expiration = 0

    def __init__(self, key, value, **args):
        super().__init__(key, **args)

        self.value = value
        self.expiration = self.get_arg_value(key="expiration", default_value=self.expiration)

    def params(self):
        return [
            self.key,
            self.value,
            self.group,
            self.expiration,
        ]

    def get_excluded_attrs(self):
        return super().get_excluded_attrs() + [
            "value",
            "expiration",
        ]
