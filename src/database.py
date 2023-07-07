from typing import Optional

# import json
# from rich import print

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


"""
def populate_defaults():
    global DEFAULTS_DB
    with open("template.json", "r") as template_json:
        template = json.load(template_json)

    tabs = list(template.keys())

    for tab in tabs:
        for k in template[tab]:
            for i in k.items():
                parameter = i[0]

                color_data = i[1]["default"]
                optional = i[1]["optional"]

                if isinstance(color_data, list):
                    color_data.append(255) if len(color_data) == 3 else None

                    r, g, b, a = color_data
                    DEFAULTS_DB.insert(
                        {
                            "parameter": parameter,
                            "category": tab,
                            "value": {
                                "red": r,
                                "green": g,
                                "blue": b,
                                "alpha": a,
                            },
                            "optional": optional,
                        },
                    )

                else:
                    DEFAULTS_DB.insert(
                        {
                            "parameter": parameter,
                            "category": tab,
                            "value": color_data,
                            "optional": optional,
                        }
                    )


if __name__ == "__main__":
    DEFAULTS_DB.truncate()
    populate_defaults()
    print(DEFAULTS_DB.all())
"""
