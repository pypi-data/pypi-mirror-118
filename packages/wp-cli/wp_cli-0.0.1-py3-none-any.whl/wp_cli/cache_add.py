from wp.cache_set import CacheSet


# TODO Test.
# Adds a value to the object cache.
# Errors if a value already exists for the key, which means the value can’t be added.
# wp cache add my_key my_group my_value 300
# Success: Added object 'my_key' in group 'my_value'.
class CacheAdd(CacheSet):
    command = ['cache', 'add']
