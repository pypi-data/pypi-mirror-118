from wp.cache_decr_incr import CacheDecrIncr


# TODO Test.
# Decrements a value in the object cache.
# Errors if the value can’t be decremented.
# wp cache decr my_key 2 my_group
# 48
class CacheDecr(CacheDecrIncr):
    command = ['cache', 'decr']
