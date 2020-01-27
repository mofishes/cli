#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
from util import run, find_exts, root_path, third_party_path

clang_format_path = os.path.join(third_party_path, "python_packages",
                                 "clang_format", "bin", "clang-format")
yapf_path = os.path.join(third_party_path, "python_packages", "bin", "yapf")


def main():
    os.chdir(root_path)

    parser = argparse.ArgumentParser()
    parser.add_argument("--py", help="run yapf", action="store_true")
    parser.add_argument("--cc", help="run clang format", action="store_true")
    args = parser.parse_args()

    did_fmt = False
    if args.py:
        yapf()
        did_fmt = True
    if args.cc:
        clang_format()
        did_fmt = True

    if not did_fmt:
        yapf()
        clang_format()


def yapf():
    print("yapf")


def clang_format():
    print("clang_format")
    run([clang_format_path, "-i", "-style", "Google"] +
        find_exts(["src", "test"], [".cpp", ".hpp"]))


if __name__ == "__main__":
    sys.exit(main())
