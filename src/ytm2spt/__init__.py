import sys


def main():
    if len(sys.argv) > 1:
        from .cli import main
    else:
        from .gui import main

    main()


if __name__ == "__main__":
    main()