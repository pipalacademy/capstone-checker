from typing import Any


class CheckStatus:
    status: str = "pass"
    message: str = ""

    def __init__(self, status: str, message: str):
        self.status = status
        self.message = message

    def dict(self):
        return {
            "status": self.status,
            "message": self.message,
        }

    @classmethod
    def fail(cls, message: str):
        return cls("fail", message)

    @classmethod
    def error(cls, message: str):
        return cls("error", message)

    @classmethod
    def pass_(cls, message: str):
        return cls("pass", message)


class ValidationError(Exception):
    pass


def run_check(
        name: str,
        context: dict[str, Any],
        args: dict[str, Any]) -> CheckStatus:
    """
    Each check should be defined like this:

    ```
    @register_check()
    def check_name(context: dict, args: dict) -> Any:
        ...

    # OR

    @regiser_check("check_name")
    def this_name_wont_matter(context: dict, args: dict) -> Any:
        ...
    ```

    If the check fails, it should raise a `ValidationError` with a message.
    Any other exception will set the status of the check to "error".
    """
    try:
        CHECKS[name](context, args)
    except ValidationError as e:
        return CheckStatus.fail(str(e))
    except Exception as e:
        # TODO: maybe log the whole traceback?
        return CheckStatus.error(str(e))
    else:
        return CheckStatus.pass_("")


CHECKS = {}
def register_check(name=None):
    def decor(f):
        CHECKS[name or f.__name__] = f
        return f
    return decor


def has_check(name: str) -> bool:
    return name in CHECKS


def get_check(name):
    return CHECKS[name]
