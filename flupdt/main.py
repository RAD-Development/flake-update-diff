#!/usr/bin/env python3

from flupdt.flake_show import get_derivations
from flupdt.cli import parse_inputs
from flupdt.flake_eval import evaluate_output
from flupdt.common import configure_logger
import logging

def main():
    configure_logger("INFO")
    args = parse_inputs()
    flake_path = args.flake_path
    derivations = get_derivations(flake_path)
    if not args.keep_hydra and len(list(filter(lambda s: s.startswith("hydraJobs"), derivations))) > 0:
        logging.info("--keep-hydra flag is not specified, removing Hydra jobs")
        derivations = filter(lambda s: not s.startswith("hydraJobs"), derivations)
    logging.info(f"derivations: {list(derivations)}")
    for d in derivations:
        evaluate_output(flake_path, d)


if __name__ == "__main__":
    main()
