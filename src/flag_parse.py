import argparse
import os
import sys
from src.algo import decode

import config.cfg as cfg
from src.algo import encode

parser = argparse.ArgumentParser(
    prog="haffman.py",
    description="Haffman encoding app",
)
actions = parser.add_argument_group("Actions")
actions.add_argument(
    "-e",
    "--encode",
    dest="enc",
    help="Encodes data",
    action="store_const",
    const=encode,
)
actions.add_argument(
    "-d",
    "--decode",
    dest="dec",
    help="Decodes data",
    action="store_const",
    const=decode,
)
parser.add_argument(
    "data",
    nargs="?",
    help="Input data",
    action="store",
)

parser.add_argument(
    "-i",
    "--input",
    type=open,
    default=None,
    metavar="path",
    help="The input file",
    action="store",
)
parser.add_argument(
    "-o",
    "--output",
    type=argparse.FileType("w"),
    default=sys.stdout,
    metavar="path",
    help="The output file",
    action="store",
)

parser.add_argument(
    "-t",
    "--table",
    type=str,
    metavar="path",
    default=None,
    help="The table input/output file",
    action="store",
)

args: argparse.Namespace = parser.parse_args()


def flag_parse():
    if args.enc is None and args.dec is None:
        raise ValueError("You must specify action!")
    elif (args.enc is None) == (args.dec is None):
        raise ValueError("You must specify only one action!")

    cfg.INPUT_FILE = args.input
    cfg.IS_INPUT_FILE = args.input is not None

    if args.data is None and not cfg.IS_INPUT_FILE:
        raise ValueError("Must be specified either input file or data!")

    cfg.OUTPUT_FILE = args.output

    if args.table is not None:
        if not os.path.exists(args.table):
            open(args.table, "w").close()
        cfg.TABLE_STREAM = open(args.table, "r+")

    if args.enc is not None:
        cfg.ACTION = args.enc
    else:
        if args.table is None:
            raise ValueError("When \'-d\' flag is set, \'-t\' flag must also be set!")
        cfg.ACTION = args.dec
