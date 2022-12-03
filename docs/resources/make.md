# Make

## For Users

- `make help`: Print this file
- `make install`: Install all
- `make install-bin`: Install executable file
- `make install-man`: Install Man page
- `make install-completions`: Install all completions
- `make install-bash-completion`: Install completion for bash
- `make install-zsh-completion`: Install completion for zsh
- `make install-tcsh-completion`: Install completion for tcsh

## For Developers

- `make install-bin-editable`: Install executable file in editable mode
- `make clean`: Remove all generated files
- `make test`: Run test, in github action
- `make dist`: Build python wheel, in github action
- `make build-docs`: Build sphinx documents, in readthedocs
- `make doc`: Build vim documents, in pre-commit hook

Before `make test`, `make dist`, `make build-docs` and `make doc`, must make
sure `translate-shell` has been correctly installed.
