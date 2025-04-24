import breadmake

bm = breadmake.BreadMake()

CC = bm.shell("which gcc")

@bm.target
def my_help() -> bool:
    bm.run("build")
    print("usage: do thing [1] .. [N]")
    return True

@bm.target
def build() -> bool:
    """
    build the exec using clang/gcc
    """
    print("build thing")
    print(f"{CC}")
    return True

if __name__ == "__main__":
    bm.compile()
