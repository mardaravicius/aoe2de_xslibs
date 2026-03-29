import subprocess
from pathlib import Path
from types import ModuleType

import xs.binary_functions as binary_functions
import xs.bool_list as bool_list
import xs.float_list as float_list
# import xs.int_int_dict as int_int_dict_v1
# import xs.int_int_dict2 as int_int_dict_v2
import xs.int_int_dict3 as int_int_dict
import xs.int_list as int_list
import xs.string_list as string_list
import xs.vector_list as vector_list
from xs_converter.converter import PythonToXsConverter


def main() -> None:
    xs_modules: list[tuple[ModuleType, str]] = [
        (int_list, "intList"),
        (float_list, "floatList"),
        (bool_list, "boolList"),
        (string_list, "stringList"),
        (int_int_dict, "intIntDict"),
        # (int_int_dict_v1, "intIntDict"),
        # (int_int_dict_v2, "intIntDict"),
        (vector_list, "vectorList"),
        (binary_functions, "binaryFunctions"),
    ]
    for module, name in xs_modules:
        xs = PythonToXsConverter.to_xs_file(module, indent=True)
        path = Path("..") / ".." / "xs" / (name + ".xs")
        write_xs_file(path, xs)
        result = subprocess.run(["xs-check", str(path.resolve()), "--ignores", "DiscardedFn"])
        if result.returncode != 0:
            raise Exception(result.returncode)


def write_xs_file(path: Path, data: str):
    with open(path, "w") as file:
        file.write(data)


if __name__ == "__main__":
    main()
