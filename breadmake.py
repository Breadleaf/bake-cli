from typing import Callable, Dict
from inspect import signature
from sys import argv
from subprocess import run, CalledProcessError

class BreadMake:
    class Target:
        def __init__(self, func: Callable[[], bool]):
            self.func = func
            self.docs = (func.__doc__ or "no documentation").strip()

        def __repr__(self):
            return f"Target({self.func}/{self.docs})"

    builtin_functions = [
        "help",
    ]

    def __init__(self):
        self.targets: Dict[str, BreadMake.Target] = {}
        self.__default: str = "help"

        def help() -> bool:
            print(f"usage: breadmake (target [optional])")
            print("targets:")

            longest_name = len(max(self.targets.keys(), key=len))
            for name, target in self.targets.items():
                print(name.ljust(longest_name), "-", target.docs)

            return True

        self.targets.setdefault("help", BreadMake.Target(help))

    def target(self, f: Callable[[], bool]):
        f_signat = signature(f)

        # ensure correct number of parameters
        f_params = f_signat.parameters
        assert len(f_params) == 0, "targets cannot have arguments"

        # ensure correct return type
        f_return = f_signat.return_annotation
        assert f_return is bool, "targets must return bool"

        # ensure target name is not builtin function
        assert \
            f.__name__ not in BreadMake.builtin_functions, \
            f"target name: {f.__name__} is taken by a built in function"

        # set target and set default if not set
        self.targets.setdefault(f.__name__, BreadMake.Target(f))
        if not self.__default:
            self.__default = f.__name__

    def default(self, name):
        assert \
            name in self.targets.keys(), "default target must be a valid target"
        self.__default = name

    def run(self, name):
        target = self.targets.get(name, None)
        assert target, f"invalid target name: {name}"
        if not target.func():
            print(f"target: {target.func.__name__} failed")
            exit(1)

    def shell(self, command: str) -> str:
        try:
            process = run(
                command, shell=True, capture_output=True, text=True, check=False
            )

            process.check_returncode()
            return str(process.stdout).strip()
        except CalledProcessError as ex:
            print(str(ex.stderr).strip())
            print(ex)
            exit(1)

    def compile(self):
        match len(argv) - 1:
            case 0: # run the default target
                self.run(self.__default)
            case 1: # run the user defined target
                self.run(argv[1])
            case _:
                print(f"usage: {argv[0]} [target]")
                print("targets:")
                print(self.targets)
                exit(1)

    def __repr__(self):
        return str(self.targets)
