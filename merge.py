import argparse
import logmerger


def merge():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar="N", type=int, nargs="+", help="log filenames")
    

if __name__ == "__main__":
    merge()
