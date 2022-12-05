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
- `make install-desktop-entry`: Install desktop entry

## For Developers

- `make clean`: Remove all untracked generated files
- `make test`: Run test, in github action
- `make build-docs`: Build sphinx documents, in readthedocs
- `make doc/*.txt`: Build vim documents, in pre-commit hook
- `make install-bin-editable`: Install executable file in editable mode. Before
  `make test`, `make build-docs`, `trans` must be installed
  correctly. So you can `make install-bin-editable XXX`. Don't `pip install -e .`
  directly, because some python files need to be updated by `make`.
