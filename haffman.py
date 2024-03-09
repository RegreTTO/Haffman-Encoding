#!/bin/env python
import sys
from src.algo import decode, encode
import config.cfg as cfg
from src.flag_parse import flag_parse
from src.flag_parse import args
from src.algo import EncodeData


def read_data() -> str:
    data: str = None
    if cfg.IS_INPUT_FILE:
        data: str = cfg.INPUT_FILE.read().strip()
        cfg.INPUT_FILE.close()
    else:
        data = args.data
    return data


def main():
    flag_parse()
    data = read_data()
    ret_data = None
    if cfg.ACTION == encode:
        ret_data = cfg.ACTION(data)
    elif cfg.ACTION == decode:
        table = cfg.TABLE_STREAM.read()
        ret_data = cfg.ACTION(data, table)
    if isinstance(ret_data, EncodeData):
        ret_data: EncodeData
        if cfg.TABLE_STREAM == sys.stdout:
            cfg.TABLE_STREAM.write("ENCODING TABLE:\n")
        for k, v in ret_data.table.items():
            cfg.TABLE_STREAM.write(f"{k} -- {v}\n")
        if cfg.OUTPUT_FILE == sys.stdout:
            cfg.OUTPUT_FILE.write(f"Encoded data: ")
        cfg.OUTPUT_FILE.write(f"{ret_data.data}")
    else:
        ret_data:str
        if cfg.OUTPUT_FILE == sys.stdout:
            cfg.OUTPUT_FILE.write("Decoded data: ")
        cfg.OUTPUT_FILE.write(ret_data)
    cfg.INPUT_FILE.close()
    cfg.OUTPUT_FILE.close()
    cfg.TABLE_STREAM.close()


if __name__ == "__main__":
    main()
