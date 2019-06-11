import argparse
import logmerger
import sys


def merge():
    parser = argparse.ArgumentParser(
        description="merge multiple log files into one with respect of date and level"
    )
    parser.add_argument(
        "level", type=str, default=logmerger.LOG_LEVELS[0], choices=logmerger.LOG_LEVELS
    )
    parser.add_argument("files", type=str, nargs="+", help="log filenames")
    args = parser.parse_args()

    for log in logmerger.parse_logs(files=args.files, level=args.level):
        print(log, file=sys.stdout, end="")


if __name__ == "__main__":
    merge()
