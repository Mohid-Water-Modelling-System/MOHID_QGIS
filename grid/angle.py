"""
The Angle class is a child of the float class.
It holds the value of the grid angle.
"""
class Angle(float):

    """
    The toString function is used to write the angle of the grid in MOHID format.
    The string is built according to the first argument of the function, which is
    the configuration provided in form of a dictionary.
    This configuration was previously read from the config.json file.
    """
    def toString(self, config: dict) -> str:
        fmt = config["fmt"]
        key = config["keys"][type(self).__name__]
        return fmt.format(key, str(self))