# import os
import sys
import subprocess


def main():
    argv = sys.argv[1:]
    p = subprocess.Popen(argv, stdin=sys.stdin, stdout=subprocess.PIPE,
                         stderr=sys.stderr)
    while p.poll() is None:
        c = p.stdout.read(1).decode(sys.stdout.encoding)
        sys.stdout.write(c)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
