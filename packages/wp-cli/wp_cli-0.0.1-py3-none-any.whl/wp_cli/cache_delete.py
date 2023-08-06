from wp.cache_get import CacheGet


# TODO Test.
# Removes a value from the object cache.
# Errors if the value can’t be deleted.
# wp cache delete my_key my_group
# Success: Object deleted.
class CacheDelete(CacheGet):
    command = ['cache', 'delete']

