#!/usr/bin/env python3

from app.flake_show import get_derivations

def main():
    print(get_derivations("/home/alice/.gitprojects/nix-dotfiles"))

if __name__ == "__main__":
    main()

