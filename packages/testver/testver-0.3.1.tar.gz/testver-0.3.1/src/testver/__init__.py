"Programmatically edit python package versions for testing."
import ast
import datetime
import astunparse
from pathlib import Path

__version__ = "0.3.1"


def modver(filepath: Path, varname="__version__", mode="string"):

    if mode == "string":
        temp_ver = datetime.datetime.now().strftime("%Y.%m.%d.a%H.dev%M")
    elif mode == "tuple":
        temp_ver = tuple(datetime.datetime.now().utctimetuple())
        temp_ver = tuple(
            [item for item in temp_ver[:-1]] + [f"dev{temp_ver[-1]}"]
        )

    filepath = Path(filepath)
    tree = ast.parse(filepath.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and (node.targets[0].id == varname):
            node.value = ast.Constant(value=temp_ver)
            # if isinstance(node.value, ast.Constant):
            #     # python >=3.8 doesn't have ast.Str
            #     # new_value = node.value.value + f"-{suffix}"
            #     node.value.value = temp_ver
            #     # new_value = node.value.value
            # elif isinstance(node.value, ast.Str):
            #     node.value.s = temp_ver
            #     # new_value = node.value.s
            break
    else:
        raise ValueError(
            f"The specified file doesn't have a variable called {varname}."
        )
    return (astunparse.unparse(tree), temp_ver)
