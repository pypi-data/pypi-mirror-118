from wp.cache_decr_incr import CacheDecrIncr


# TODO Test.
# Increments a value in the object cache.
# wp cache incr my_key 2 my_group
# 50
class CacheIncr(CacheDecrIncr):
    command = ['cache', 'incr']
