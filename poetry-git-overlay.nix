{ pkgs }:
final: prev: {

  rad-development-python = prev.rad-development-python.overridePythonAttrs (_: {
    src = pkgs.fetchgit {
      url = "https://github.com/RAD-Development/rad-development-python";
      rev = "4ee897ab983234eda6f12dfcfd822bffab01f740";
      sha256 = "1hxdqnjrznx0c07qn5cdx7p7f7sz2ysydx5l82w0r7rdadj69ik2";
    };
  });

}
