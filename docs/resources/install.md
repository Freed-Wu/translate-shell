# Install

## [AUR](https://aur.archlinux.org/packages/python-translate-shell)

```sh
yay -S python-translate-shell
```

## [Nix](https://nixos.org)

For NixOS, add the following code to `/etc/nixos/configuration.nix`:

```nix
{ config, pkgs, ... }:
{
  nix.settings.experimental-features = [ "flakes" ];
  environment.systemPackages =
    let
      translate-shell = (
        builtins.getFlake "github:Freed-Wu/translate-shell"
      ).packages.${builtins.currentSystem}.default;
    in
    [
      translate-shell
    ];
}
```

For nix,

```sh
nix shell github:Freed-Wu/translate-shell
```

Or just take a try without installation:

```sh
nix run github:Freed-Wu/translate-shell -- --help
```

## [PYPI](https://pypi.org/project/translate-shell)

```sh
pip install translate-shell
```

See [requirements](requirements) to know `extra_requires`.
