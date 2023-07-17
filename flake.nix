{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.python-setuptools-generate.url = "github:Freed-Wu/setuptools-generate";
  inputs.python-repl-python-wakatime.url = "github:wakatime/repl-python-wakatime";
  outputs = { self, nixpkgs, flake-utils, python-setuptools-generate, python-repl-python-wakatime }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let setuptools-generate = python-setuptools-generate.packages.${system}.default; in
        let repl-python-wakatime = python-repl-python-wakatime.packages.${system}.default; in
        with nixpkgs.legacyPackages.${system};
        with python3.pkgs;
        {
          formatter = nixpkgs-fmt;
          packages.default = buildPythonApplication rec {
            name = "translate-shell";
            src = self;
            format = "pyproject";
            disabled = pythonOlder "3.6";
            propagatedBuildInputs = [
              colorama
              keyring
              langdetect
              # https://github.com/NixOS/nixpkgs/issues/241694
              # py-notifier
              rich
              pystardict
              repl-python-wakatime
              pyyaml
              jinja2
              openai
              # https://github.com/NixOS/nixpkgs/issues/224921
              # llama-cpp
            ];
            nativeBuildInputs = [
              setuptools-generate
            ];
            pythonImportsCheck = [
              "translate_shell"
            ];
            meta = {
              mainProgram = "trans";
            };
          };
        }
      );
}
