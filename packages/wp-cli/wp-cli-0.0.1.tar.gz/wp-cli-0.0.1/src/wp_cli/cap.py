from wp.command import WPCommand


# TODO Test.
# Base to a couple cap commands.
class Cap(WPCommand):
    command = ['cap']

    # <role>
    # Key for the role.
    role = ""

    # <cap>…
    # One or more capabilities to add.
    cap = ""

    def __init__(self, role, cap, **args):
        super().__init__(**args)

        self.value = role
        self.value = cap

    def params(self):
        return [
            self.role,
            self.cap,
        ]

    def get_excluded_attrs(self):
        return [
            "role",
            "cap",
        ]
