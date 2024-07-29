#!/usr/bin/env python3
import argparse


def parse_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "flake_path", metavar="flake-path", help="path to flake to evaluate"
    )
    args = parser.parse_args()
    return args
