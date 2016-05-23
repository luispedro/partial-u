let
  pkgs = import <nixpkgs> {};
in
{ stdenv ? pkgs.stdenv, python ? pkgs.python27, pythonPackages ? pkgs.python27Packages }:

let
  jug = import ../jug { inherit python pythonPackages ; };
in
  stdenv.mkDerivation {
     name = "partialUenv";
     version = "0.0.0";
     src = ./.;
     propagatedBuildInputs = with pythonPackages; [
            pkgs.readline6
            pkgs.python
            pkgs.liblapack
            pkgs.R
            pkgs.rPackages.npsm
            sqlite3
            rpy2
            ipython
            numpy
            scipy
            pandas
            matplotlib
            pyside
            virtualenv
            jug
            pkgs.zsh
            ];
}



