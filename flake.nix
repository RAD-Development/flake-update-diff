{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pre-commit-hooks = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        # nixpkgs-stable.follows = "nixpkgs-stable";
        # flake-compat.follows = "flake-compat";
      };
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      pre-commit-hooks,
      ...
    }@inputs:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        pkgs = nixpkgs.legacyPackages.${system};
        poetry2nix = inputs.poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };

        overrides = poetry2nix.overrides.withDefaults (
          _final: prev: {
            # prefer binary wheels instead of source distributions for rust based dependencies
            # avoids needing to build them from source. technically a security risk
            polars = prev.polars.override { preferWheel = true; };
            ruff = prev.ruff.override { preferWheel = true; };
            greenlet = prev.greenlet.override { preferWheel = true; };
            sqlalchemy = prev.sqlalchemy.override { preferWheel = true; };
          }
        );

        poetryConfig = {
          inherit overrides;
          projectDir = self;
          python = pkgs.python312;
        };
      in
      rec {
        packages = {
          myapp = poetry2nix.mkPoetryApplication poetryConfig // {
            develop = true;
          };
          default = self.packages.${system}.myapp;
        };

        formatter = pkgs.nixfmt-rfc-style;

        devShells = import ./shell.nix {
          inherit
            self
            poetryConfig
            poetry2nix
            inputs
            system
            checks
            ;
        };
        checks = import ./checks.nix { inherit inputs system formatter; };
      }
    )
    // {
      hydraJobs = import ./hydra/jobs.nix { inherit (self) inputs outputs; };
    };
}
