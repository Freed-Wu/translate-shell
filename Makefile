PREFIX = /usr
BINNAME = trans
THEMIS = themis
LIBNAME = translate-shell
LIBPATH = src/$(subst -,_,$(LIBNAME))
MANPATH = $(PREFIX)/share/man/man1/$(BINNAME).1.gz
BASH_COMPLETION = $(PREFIX)/share/bash-completion/completions/$(BINNAME)
ZSH_COMPLETION = $(PREFIX)/share/zsh/site-functions/_$(BINNAME)
TCSH_COMPLETION = /etc/profile.d/$(BINNAME).csh
DESKTOP_ENTRY = $(PREFIX)/share/applications/translate-shell.desktop
ICON = $(PREFIX)/share/$(LIBNAME)/images/icon.png
MARKDOWN = $(shell find . -type f -name '*.md')
EXTERNAL_MAIN_PY = $(shell find $(LIBPATH)/external/* -name __main__.py -not -wholename '*/shtab/*')
EXTERNAL_INIT_PY = $(addsuffix __init__.py,$(dir $(EXTERNAL_MAIN_PY)))
IGNORE_PY = $(LIBPATH)/_version.py $(LIBPATH)/_metainfo.py
GENERATE_PY = $(EXTERNAL_INIT_PY) $(IGNORE_PY)
SRC = $(shell find $(LIBPATH) -type f -name '*.py') \
			$(GENERATE_PY) \
			$(shell find $(LIBPATH)/assets -type f -name '*') \
			pyproject.toml

.PHONY: default
default: install

# build {{{ #
.PHONY: build
build:
	python -m build

src/translate_shell/_version.py: build
src/translate_shell/_metainfo.py: build templates/metainfo.py

pyproject.toml: scripts/generate-pyproject.toml.pl requirements/*.txt
	$^ $@

CITATION.cff: scripts/generate-CITATION.cff.pl pyproject.toml
	$^ $@

src/translate_shell/external/%/__init__.py: scripts/generate-__init__.py.pl
	$^ $@ src/translate_shell/external/shtab/__init__.py > $@
# }}} build #

# build-docs {{{ #
.PHONY: build-docs
build-docs: docs/conf.py $(MARKDOWN) $(SRC)
	cd docs && sphinx-build . _build/html

docs/resources/requirements.md: scripts/generate-requirements.md.sh requirements/*.txt
docs/resources/man.md: build/resources/trans.1.md
docs/resources/translator.md: scripts/generate-translator.md.py $(SRC)
docs/resources/config.md: examples/config.py $(SRC)
docs/resources/vim.md: scripts/generate-vim.md.sh doc/*.txt
docs/misc/acknowledges.md: scripts/generate-acknowledges.md.sh $(SRC)
docs/misc/todo.md: scripts/generate-todo.md.sh $(SRC)
docs/api/%.md: scripts/generate-api.md.sh $(SRC)

addon-info.json: scripts/generate-addon-info.json.pl pyproject.toml
	$^ $@

doc/%.txt: addon-info.json $(shell find . -type f -name '*.vim')
	pre-commit run vimdoc
# }}} build-docs #

# install {{{ #
.PHONY: install
install: install-man install-completions install-desktop-entry
	pip install -e .

.PHONY: install-man
build/resources/trans.1.gz: build
install-man: build/resources/trans.1.gz
	install -Dm644 $< $(MANPATH)

.PHONY: install-completions
install-completions: install-bash-completion install-zsh-completion install-tcsh-completion

.PHONY: install-bash-completion
build/resources/trans: build
install-bash-completion: build/resources/trans
	install -Dm644 $< $(BASH_COMPLETION)

.PHONY: install-zsh-completion
build/resources/_trans: build
install-zsh-completion: build/resources/_trans
	install -Dm644 $< $(ZSH_COMPLETION)

.PHONY: install-tcsh-completion
build/resources/trans.csh: build
install-tcsh-completion: build/resources/trans.csh
	install -Dm644 $< $(TCSH_COMPLETION)

.PHONY: install-desktop-entry
install-desktop-entry: assets/desktop/*.desktop $(LIBPATH)/assets/images/icon.png
	install -D $< $(DESKTOP_ENTRY)
	install -D $(wordlist 2,2,$^) $(ICON)
# }}} install #

.PHONY: uninstall
uninstall:
	rm -rf $(BASH_COMPLETION) $(ZSH_COMPLETION) $(TCSH_COMPLETION) $(MANPATH) \
		$(DESKTOP_ENTRY) $(ICON)
	pip uninstall $(LIBNAME)

.PHONY: clean
clean:
	rm -rf docs/_build $(IGNORE_PY) src/*.egg-info dist build

.PHONY: test
test:
	$(THEMIS)
	pytest --cov
	pre-commit run -a

.PHONY: help
help:
	@cat docs/resources/make.md
# ex: foldmethod=marker
