#!/usr/bin/python3
#codeName: autoQuery.py
#Author: Dahir Muhammad Dahir
#Date: 19th-November-2018
#About: script for automatically issuing queries to target vulnerable
#       to sql Injection and supporting stacked queries

import os
import base64
import argparse

thisDir = os.getcwd()

def main():
    parser = argparse.ArgumentParser(description="decode base64 encoded text")
    parser.add_argument("-f", "--file", help="file containing the base64 encoded text", required=True)
    parser.add_argument("-o", "--output", help="file to output the decoded text")
    args = parser.parse_args()
    decode(args.file, args.output)


def decode(file, output=""):
    if not output:
        output = "{}_decoded.dmd".format(file)

    clean_encoded_lines = []
    with open(thisDir+"/{}".format(output), "w") as f:
        with open(file, "r") as x:
            encoded_lines = x.readlines()
        
        for line in encoded_lines:
            line = line.strip("\n")
            clean_encoded_lines.append(line)
        
        text = "".join(clean_encoded_lines)
        decoded_text = base64.b64decode(text)
        f.write(str(decoded_text))
        print("Done....decoding {}".format(output))


if __name__=="__main__":
    main()
