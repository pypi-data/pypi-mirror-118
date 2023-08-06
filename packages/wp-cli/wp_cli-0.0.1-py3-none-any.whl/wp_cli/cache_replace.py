from wp.cache_set import CacheSet


# TODO Test.
# Replaces a value in the object cache, if the value already exists.
# Errors if the value can’t be replaced.
# wp cache replace my_key new_value my_group
# Success: Replaced object 'my_key' in group 'my_group'.
class CacheReplace(CacheSet):
    command = ['cache', 'replace']
