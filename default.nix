{ lib, python3, fetchurl }:

with python3.pkgs;

buildPythonApplication rec {
  pname = "translate-shell";
  version = "0.0.19";
  format = "wheel";
  disabled = pythonOlder "3.6";

  src = fetchurl {
    url = "https://github.com/Freed-Wu/translate-shell/releases/download/${version}/translate_shell-0.0.19-py3-none-any.whl";
    sha256 = "N9vRS9zZMX02yuXEfaQQuDvw8fY+OjjLUNbsG5typgM=";
  };

  propagatedBuildInputs = [
    colorama
    keyring
    langdetect
    # py-notifier
    rich
    # pystardict
    # repl-python-wakatime
    pyyaml
  ];

  nativeCheckInputs = [
    setuptools
  ];

  pythonImportsCheck = [
    "translate_shell"
  ];

  postInstall =
    let
      bin = "trans";
      bash =
        fetchurl
          {
            url = "https://github.com/Freed-Wu/translate-shell/releases/download/${version}/trans";
            sha256 = "OhEeQIYVZq9H8MRAyNWYn5/Vlxv01XeJ2MLgzOgc8tw=";
          }
      ;
      zsh =
        fetchurl
          {
            url = "https://github.com/Freed-Wu/translate-shell/releases/download/${version}/_trans";
            sha256 = "q402/8M3NFtqzthugFDVqBs2dZDm04Q96ZWmVrboWW4=";
          }
      ;
      tcsh =
        fetchurl
          {
            url = "https://github.com/Freed-Wu/translate-shell/releases/download/${version}/trans.csh";
            sha256 = "qALgfq1juIoAAOBVaB8XbKtoRLZrei7lYiClM+eIwmE=";
          }
      ;
      man =
        fetchurl
          {
            url = "https://github.com/Freed-Wu/translate-shell/releases/download/${version}/trans.1.gz";
            sha256 = "BqUhHhkTvsgK5Qmfd8I9e/jx9Y3Nd+somP8M68KOhoI=";
          }
      ;
      desktop =
        fetchurl
          {
            url = "https://github.com/Freed-Wu/translate-shell/blob/main/assets/desktop/translate-shell.desktop";
            sha256 = "/U2mdaNxMtx9N6n7KVf23WmmqixTWC5XaDxq5+9iuSE=";
          }
      ;
    in
    ''
      install -Dm644 ${bash} $out/share/bash-completion/completions/${bin}
      install -Dm644 ${zsh} $out/share/zsh/site-functions/_${bin}
      install -Dm644 ${tcsh} $out/etc/profile.d/${bin}.csh
      install -Dm644 ${man} $out/share/man/man1/${bin}.1
      install -Dm644 ${desktop} $out/share/applications/${pname}.desktop
      install -Dm644 $out/lib/python*/site-packages/*/assets/images/${pname}.png -t $out/share/icons/hicolor/36x36/apps
    '';

  meta = with lib; {
    description = "Translate text by google, bing, youdaozhiyun, haici, stardict, etc at same time from CLI, GUI (GNU/Linux, Android, macOS and Windows), REPL, python, shell and vim";
    homepage = "https://translate-shell.readthedocs.io";
    downloadPage = "https://pypi.org/project/translate-shell/#files";
    changelog = "https://translate-shell.readthedocs.io/en/latest/misc/changelog.html";
    license = licenses.gpl3;
    mainProgram = "trans";
    # override translate-shell (awk)
    priority = 99;
    platforms = platforms.all;
  };
}
