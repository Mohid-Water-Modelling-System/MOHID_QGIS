class Angle(float):
    def toString(self, config: dict) -> str:
        fmt = config["fmt"]
        key = config["keys"][type(self).__name__]
        return fmt.format(key, str(self))