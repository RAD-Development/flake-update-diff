#!/usr/bin/env python3

import json
from app.common import bash_wrapper
import shutil


def traverse_json_base(json_dict: dict, path: list[str]):
    final_paths = []
    for key, value in json_dict.items():
        if isinstance(value, dict):
            keys = value.keys()
            if "type" in keys and value["type"] in [
                "nixos-configuration",
                "derivation",
            ]:
                final_paths += [".".join(path + [key])]
            else:
                final_paths += traverse_json_base(value, path + [key])
    return final_paths


def traverse_json(json_dict: dict):
    return traverse_json_base(json_dict, [])


def get_derivations(path_to_flake: str):
    nix_path = shutil.which("nix")
    flake_show = bash_wrapper(f"{nix_path} flake show --json", path=path_to_flake)
    if flake_show[1] != 0:
        raise RuntimeError("flake show returned non-zero exit code")
    flake_show_json = json.loads(flake_show[0])
    derivations = traverse_json(flake_show_json)
    return derivations
