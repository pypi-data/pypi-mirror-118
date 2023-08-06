import os
import argparse
import pathlib
from . import modver


parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "file",
    type=str,
    help="The file to read in and modify.",
)
parser.add_argument(
    "--varname", type=str, default="__version__", required=False
)
parser.add_argument(
    "--mode",
    type=str,
    default="string",
    choices=["string", "tuple"],
    required=False,
)
parser.add_argument("--dryrun", action="store_true")


def _get_sha():
    return os.getenv("GITHUB_SHA") or os.getenv("TRAVIS_COMMIT") or "test"


def main():
    sha = _get_sha()

    args = parser.parse_args()
    filepath = pathlib.Path(args.file)
    varname = args.varname
    mode = args.mode

    if filepath.is_dir():
        files_to_try = sorted(
            [file_ for file_ in sorted(filepath.glob("**/__init__.py"))]
            + [file_ for file_ in sorted(filepath.glob("**/__version__.py"))]
        )
        for file_ in files_to_try:
            if varname in file_.read_text():
                filepath = file_
                break
        else:
            raise FileNotFoundError(
                f"Could not find a file that contained the variable {varname}"
            )
    mod_text, new_ver = modver(filepath, varname=varname, mode=mode)
    if not args.dryrun:
        filepath.write_text(mod_text)
        print(f"Changed {varname} in file {filepath} to {new_ver}")
    else:
        print(f"Would have changed {varname} in file {filepath} to {new_ver}")


if __name__ == "__main__":

    main()
