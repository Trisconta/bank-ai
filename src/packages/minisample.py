""" minisample.py

Shows usage of `BankMov` class.
"""

import sys
import bankai
import bankai.bmovement
import bankai.imovement


def main():
    """ Main script """
    res, msg = do_script(sys.argv[1:])
    print(msg, end="")
    sys.exit(1 if msg else 0)


def do_script(args):
    """ Script function """
    param = args if args else ["comprovativo.txu"]
    tup = do_run(param)
    return tup


def do_run(param):
    fname, rest = param[0], param[1:]
    assert not rest, "Unexpected parameters!"
    mov = bankai.bank.BankMov(fname)
    btp = mov.get_me()
    lst = btp.content()
    #print(*lst[-5:], sep="\n")		# Last 5 movements!
    movements = [
        bankai.bmovement.Movement.from_dict(item) for item in lst
    ]
    print(*movements, sep="\n\n")
    indexed = bankai.imovement.index_movements(movements, 1001)  # indexed_... sorts out dates!
    print("+++" * 9)
    print(*indexed, sep="\n")
    return lst, ""


if __name__ == "__main__":
    main()
