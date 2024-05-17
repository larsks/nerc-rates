import sys
import pydantic

from .. import rates


def main():
    try:
        r = rates.load_from_file()
        print(f"OK [{len(r.root)} entries]")
    except pydantic.ValidationError as err:
        sys.exit(err)
