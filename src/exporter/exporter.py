import subprocess
from pathlib import Path

from xs.binary_functions import functions
from xs.float_list import float_list
from xs.int_int_dict2 import int_int_dict
from xs.int_list import int_list
from xs.string_list import string_list
from xs.vector_list import vector_list


def main(include_xs_tests: bool = False) -> None:
    xs_file_creators = [
        int_list,
        float_list,
        string_list,
        int_int_dict,
        functions,
    ]
    for fc in xs_file_creators:
        xs, name = fc(include_xs_tests)
        path = Path("..") / ".." / "xs" / (name + ".xs")
        write_xs_file(path, xs)
        result = subprocess.run(["xs-check", f'{path.resolve()}', "--ignores", "DiscardedFn"])
        if result.returncode != 0:
            raise Exception(result.returncode)


def write_xs_file(path: Path, data: str):
    with open(path, "w") as file:
        file.write(data)


if __name__ == "__main__":
    main()
