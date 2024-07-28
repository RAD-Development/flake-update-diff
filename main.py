#!/usr/bin/env python3

from app.flake_show import get_derivations

print(get_derivations("/home/alice/.gitprojects/nix-dotfiles"))
