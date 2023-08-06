class InputError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.msg = msg

    def __str__(self) -> str:
        return 'InputError: ' + self.msg


class VaildError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.msg = msg

    def __str__(self) -> str:
        return 'VaildError: ' + self.msg
