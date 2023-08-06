from wp.command import WPCommand


# Attempts to determine which object cache is being used.
# Note that the guesses made by this function are based on the WP_Object_Cache classes
# that define the 3rd party object cache extension. Changes to those classes could render
# problems with this function’s ability to determine which object cache is being used.
# wp cache type
# Default
class CacheType(WPCommand):
    command = ['cache', 'type']

    def __init__(self, **args):
        super().__init__(**args)

    def params(self):
        return []
