from wp.command import WPCommand

# Open /wp-admin/ in a browser.
# wp admin
class Admin(WPCommand):
    command = ['admin']

    def __init__(self, **args):
        super().__init__(**args)

    def params(self):
        return []
