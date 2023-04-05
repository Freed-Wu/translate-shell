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
            pname = "translate-shell";
            version = "";
            src = self;
            format = "pyproject";
            disabled = pythonOlder "3.6";
            propagatedBuildInputs = [
              colorama
              keyring
              langdetect
              # py-notifier
              rich
              # pystardict
              repl-python-wakatime
              pyyaml
            ];
            nativeCheckInputs = [
              installShellFiles
              setuptools-generate
            ];
            pythonImportsCheck = [
              "translate_shell"
            ];
            postInstall = ''
              install -Dm644 assets/desktop/translate-shell.desktop -t $out/share/applications
              install -Dm644 src/translate_shell/assets/images/translate-shell.png -t $out/share/icons/hicolor/36x36/apps
              installManPage sdist/trans.1
              installShellCompletion --cmd trans \
                --bash sdist/trans \
                --zsh sdist/_trans
            '';
          };
        }
      );
}
