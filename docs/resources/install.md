# Install

## [AUR](https://aur.archlinux.org/packages/python-translate-shell)

```sh
yay -S python-translate-shell
```

## [NUR](https://nur.nix-community.org/repos/freed-wu)

```nix
{ config, pkgs, ... }:
{
  nixpkgs.config.packageOverrides = pkgs: {
    nur = import
      (
        builtins.fetchTarball
          "https://github.com/nix-community/NUR/archive/master.tar.gz"
      )
      {
        inherit pkgs;
      };
  };
  environment.systemPackages = with pkgs;
      (
        python3.withPackages (
          p: with p; [
            nur.repos.Freed-Wu.translate-shell
          ]
        )
      )
}
```

## [Nix](https://nixos.org)

```sh
nix shell github:Freed-Wu/translate-shell
```

Run without installation:

```sh
nix run github:Freed-Wu/translate-shell -- --help
```

## [PYPI](https://pypi.org/project/translate-shell)

```sh
pip install translate-shell
```

See [requirements](requirements) to know `extra_requires`.
