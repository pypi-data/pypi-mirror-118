from wp.cap import Cap


# TODO Test.
# Adds capabilities to a given role.
# wp cap add author spectate
# Success: Added 1 capability to 'author' role.
class CapAdd(Cap):
    command = ['cap', "add"]

    # <role>
    # Key for the role.
    role = ""

    # <cap>…
    # One or more capabilities to add.
    cap = ""

    # [--grant]
    # Adds the capability as an explicit boolean value, instead of implicitly defaulting to true.
    # ---
    # default: true
    # options:
    # – true
    # – false
    # ---

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
