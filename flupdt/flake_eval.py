#!/usr/bin/env python3

import logging
from typing import Optional
from flupdt.common import bash_wrapper
import re

drv_re = re.compile(r'.*(/nix/store/.*\.drv).*')

def evaluate_output(path:str, output: str) -> Optional[str]:
    logging.info(f"evaluating {output}")
    out = bash_wrapper(f"nix eval {path}#{output}")
    logging.debug(out[0])
    logging.debug(out[1])
    logging.debug(out[2])
    if out[2] != 0:
        logging.warning(f"output {output} did not evaluate correctly")
        return None
    else:
        drv_match = drv_re.match(out[0])
        if drv_match is None:
            out_msg = "derivation succeeded but output derivation does not contain a derivation"
            raise RuntimeError(out_msg)
        drv = drv_match.group(1)
        logging.debug(f"derivation evaluated to {drv}")
