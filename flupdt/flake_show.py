#!/usr/bin/env python3

import json
from rad_development_python import bash_wrapper
import shutil
import logging
import re

output_regexes = [
    re.compile(r"checking derivation (.*)..."),
    re.compile(r"checking NixOS configuration \'(nixosConfigurations.*)\'\.\.\."),
]


def traverse_json_base(json_dict: dict, path: list[str]) -> list[str]:
    final_paths = []
    for key, value in json_dict.items():
        if isinstance(value, dict):
            keys = value.keys()
            if "type" in keys and value["type"] in [
                "nixos-configuration",
                "derivation",
            ]:
                output = ".".join(path + [key])
                final_paths += [output]
            else:
                final_paths += traverse_json_base(value, path + [key])
    return final_paths


def traverse_json(json_dict: dict) -> list[str]:
    return traverse_json_base(json_dict, [])


def get_derivations_from_check(nix_path: str, path_to_flake: str) -> list[str]:
    flake_check = bash_wrapper(f"{nix_path} flake check --verbose --keep-going", path=path_to_flake)
    if flake_check[2] != 0:
        logging.warn(
            "nix flake check returned non-zero exit code, collecting all available outputs"
        )
    error_out = flake_check[1].split("\n")
    possible_outputs = filter(lambda s: s.startswith("checking"), error_out)
    derivations = []
    for output in possible_outputs:
        for r in output_regexes:
            logging.debug(f"{output} {r.pattern}")
            match = r.match(output)
            if match is not None:
                logging.debug(match.groups())
                derivations += [match.groups()[0]]
    return derivations


def get_derivations(path_to_flake: str) -> list[str]:
    nix_path = shutil.which("nix")
    derivations = []
    if nix_path is None:
        raise RuntimeError("nix is not available in the PATH, please verify that it is installed")
    flake_show = bash_wrapper(f"{nix_path} flake show --json", path=path_to_flake)
    if flake_show[2] != 0:
        logging.error("flake show returned non-zero exit code")
        logging.warn("falling back to full evaluation via nix flake check")
        derivations = get_derivations_from_check(nix_path, path_to_flake)
    else:
        flake_show_json = json.loads(flake_show[0])
        derivations = traverse_json(flake_show_json)
    for i in range(len(derivations)):
        if derivations[i].startswith("nixosConfigurations"):
            derivations[i] += ".config.system.build.toplevel"
    return derivations
