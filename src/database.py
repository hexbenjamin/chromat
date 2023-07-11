from typing import Optional

from tinydb import TinyDB, Query


DEFAULTS_DB = TinyDB("data/defaults.json")
USER_DB = TinyDB("data/user.json")


def get_picker_settings(category: Optional[str] = None):
    Parameter = Query()
    if category is not None:
        yield from DEFAULTS_DB.search(
            (Parameter.category == category) & (Parameter.value.red.exists())
        )
    else:
        yield from DEFAULTS_DB.search(Parameter.value.red.exists())
