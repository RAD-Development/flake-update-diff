# Flake Update Diff Tool

This is the Nix flake update validator. A tool which is able to evaluate a flake
at two points in history, check that everything evaluates, and provide a diff
of the two. In its target state, it will provide a similar function to
DeterminateSystems' awesome `update-flake-lock` tool, but with `nvd` integration
and other bells and whistles that we've come to like.

## How to Use

Currently, this only supports locally-stored flakes, although we are planning to
add support for `git`-based URLs for usage outside of CI pipelines where the
repository is already downloaded.

``` shell
nix run github:RAD-Development/flake-update-diff-tool -- <path to local flake>
```

For use in other nix-based projects, `flpudt` is available as
`packages.${system}.flupdt`. Please see our `examples/` folder for common
use-cases.

## Why the name

`flupdt` comes from Fl(ake) Up(date) D(iff) T(ool). The cli is also available as
`flake-update-diff-tool`, for ease-of-use and those who use screen readers or
similar accessibility tools that may not react well to `flupdt`.

## Contributing

### Update procedure

Until `rad_development_python` (`rdp`) is in PyPI, we use the below steps to
update the lock file when there is an update to `rdp`.

1. Run `poetry lock` to update the poetry reference to GitHub
1. Run `poetry2nix lock --out .poetry-git-overlay.nix` to update the overlay
   which Poetry2Nix uses
1. Run `nix flake check` to verify that all is building as expected
