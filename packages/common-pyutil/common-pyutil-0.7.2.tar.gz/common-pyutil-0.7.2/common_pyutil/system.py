from typing import List, Dict, Union, Callable, Optional
import os
import sys
import importlib.machinery
import importlib.util
import types
import argparse


class Semver:
    def __init__(self, version_string: str):
        self._version: List[int] = [*map(int, version_string.split("."))]

    def greater_than(self, other: Union["Semver", str]) -> bool:
        if isinstance(other, str):
            other = Semver(other)
            return self.greater_than(other)
        elif isinstance(other, Semver):
            greater = False
            nolesser = True
            for x, y in zip(self._version, other._version):
                if x > y:
                    greater = True
                    break
                if y > x:
                    nolesser = False
            if len(other) < len(self):
                return nolesser or greater
            else:
                return nolesser and greater

    def equal_to(self, other: Union["Semver", str]) -> bool:
        if isinstance(other, str):
            other = Semver(other)
            return self.equal_to(other)
        else:
            return len(self) == len(other) and\
                all([x == y for x, y in zip(self._version, other._version)])

    def smaller_than(self, other: Union["Semver", str]) -> bool:
        if isinstance(other, str):
            other = Semver(other)
            return self.smaller_than(other)
        else:
            return not self.greater_than(other) and not self.equal_to(other)

    def geq(self, other: Union["Semver", str]) -> bool:
        return self.greater_than(other) or self.equal_to(other)

    def leq(self, other: Union["Semver", str]) -> bool:
        return self.smaller_than(other) or self.equal_to(other)

    def __len__(self) -> int:
        return len(self._version)

    def __repr__(self) -> str:
        return ".".join(map(str, self._version))


def which(program: str):
    """
    This function is taken from
    http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def load_user_module(modname: str, search_path: List[str] = None) -> Optional[types.ModuleType]:
    """`search_paths` is a list of paths. Defaults to `sys.path`"""
    if search_path is not None:
        spec = importlib.machinery.PathFinder.find_spec(modname, search_path)
    else:
        if modname.endswith(".py"):
            modname = modname[:-3]
        spec = importlib.machinery.PathFinder.find_spec(modname)
    if spec is None:
        print(f"Could not find module {modname}")
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    return mod
    # if spec.loader:
    #     spec.loader.exec_module(mod)
    #     return mod
    # else:
    #     return None


class hierarchical_parser:
    def __init__(self, name: str, usage: str, cmd_map: Dict[str, Callable],
                 version_str: Optional[str] = None):
        self.name = name
        self.usage = usage
        self.cmd_map = cmd_map
        self.version_str = version_str or "No version provided"

    def __call__(self):
        parser = argparse.ArgumentParser(self.name, allow_abbrev=False, add_help=False,
                                         formatter_class=argparse.RawTextHelpFormatter,
                                         usage=self.usage)
        parser.add_argument("command", help=f"""Command to run.

command is one of {", ".join(map(lambda x: f'"{x}"', self.cmd_map.keys()))}

Type "{self.name} command --help" to get help about the individual commands.""")
        if self.version_str:
            parser.add_argument("--version", action="store_true", help="Print version and exit")
        if len(sys.argv) == 1:
            print("No command given\n")
            parser.print_help()
            sys.exit(1)
        elif sys.argv[1] in {"-h", "--help"}:
            parser.print_help()
            sys.exit(0)
        elif sys.argv[1] == "--version" and self.version_str:
            print(self.version_str)
            sys.exit(0)
        try:
            args, sub_args = parser.parse_known_args()
        except Exception:
            parser.print_help()
            sys.exit(1)

        if args.command in self.cmd_map:
            self.cmd_map[args.command](sub_args)
        else:
            print(f"Unknown command \"{args.command}\"\n")
            parser.print_help()
            sys.exit(1)
