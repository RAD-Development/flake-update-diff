{ pkgs }:
final: prev: {

  rad-development-python = prev.rad-development-python.overridePythonAttrs (
    _: {
      src = pkgs.fetchgit {
        url = "https://github.com/RAD-Development/rad-development-python";
        rev = "f919535e1eb39b78f77c3c2b8ccee9244fd7fc92";
        sha256 = "0vba1d184ks4r78d9z252paxpfwvwq4h9fvhmsavby1rr2dr1976";
      };
    }
  );

}
