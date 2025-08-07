import subprocess
from pathlib import Path

from xs.int_int_dict import int_int_dict
from xs.int_list import int_list


def main(include_xs_tests: bool = False) -> None:
    xs_file_creators = [
        int_list,
        int_int_dict,
    ]
    for fc in xs_file_creators:
        xs, name = fc(include_xs_tests)
        path = Path("..") / ".." / "xs" / (name + ".xs")
        write_xs_file(path, xs)
        result = subprocess.run(["xs-check", f'{path.resolve()}', "--ignores", "DiscardedFn,NoNumPromo,FirstOprArith"])
        if result.returncode != 0:
            raise Exception(result.returncode)


def write_xs_file(path: Path, data: str):
    with open(path, "w") as file:
        file.write(data)


if __name__ == '__main__':
    main()
