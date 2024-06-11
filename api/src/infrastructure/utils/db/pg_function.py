class PGFunction:

    def __init__(self, function: str) -> None:
        self._function = function

    @property
    def function(self) -> str:
        return self._function
