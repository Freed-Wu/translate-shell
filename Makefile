PREFIX = /usr
BINNAME = trans
THEMIS = themis
LIBNAME = translate-shell
LIBPATH = src/$(subst -,_,$(LIBNAME))
MANPATH = $(PREFIX)/share/man/man1/$(BINNAME).1.gz
PRINT_COMPLETIONS = $(BINNAME) --print-completion
BASH_COMPLETION = $(PREFIX)/share/bash-completion/completions/$(BINNAME)
ZSH_COMPLETION = $(PREFIX)/share/zsh/site-functions/_$(BINNAME)
TCSH_COMPLETION = /etc/profile.d/$(BINNAME).csh
DESKTOP_ENTRY = $(PREFIX)/share/applications/translate-shell.desktop
ICON = $(PREFIX)/share/$(LIBNAME)/images/icon.png
MARKDOWN = $(shell find . -type f -name '*.md')
EXTERNAL_MAIN_PY = $(shell find $(LIBPATH)/external/* -name __main__.py)
EXTERNAL_INIT_PY = $(addsuffix __init__.py,$(dir $(EXTERNAL_MAIN_PY)))
_VERSION_PY = $(LIBPATH)/_version.py
GENERATE_PY = $(EXTERNAL_INIT_PY) $(_VERSION_PY)
SRC = $(shell find $(LIBPATH) -type f -name '*.py') \
			$(GENERATE_PY) \
			$(shell find $(LIBPATH)/assets -type f -name '*') \
			$(LIBPATH)/assets/txt/epilog.txt \
			$(LIBPATH)/assets/txt/version.txt \
			pyproject.toml setup.py
MAN_DEPENDS = scripts/$(BINNAME) $(SRC)

.PHONY: default
default: install

# build {{{ #
.PHONY: build
build: $(MAN_DEPENDS) CITATION.cff
	python -m build

%/_version.py: build

pyproject.toml: scripts/generate-pyproject.toml.py pyproject.toml.in requirements/*.txt
	$(wordlist 1,2,$^) > $@

CITATION.cff: scripts/generate-CITATION.cff.py CITATION.cff.in pyproject.toml
	$(wordlist 1,3,$^) > $@

src/translate_shell/external/%/__init__.py: scripts/generate-__init__.py.py src/translate_shell/external/%/__main__.py templates/__init__.py
	$(wordlist 1,3,$^) > $@

src/translate_shell/assets/txt/epilog.txt: scripts/generate-epilog.txt.py pyproject.toml templates/epilog.txt
	$(wordlist 1,3,$^) > $@

src/translate_shell/assets/txt/version.txt: scripts/generate-version.txt.py pyproject.toml templates/version.txt
	$(wordlist 1,3,$^) > $@

src/translate_shell/assets/txt/description.txt: scripts/generate-description.txt.py pyproject.toml
	$(wordlist 1,2,$^) > $@
# }}} build #

# build-docs {{{ #
.PHONY: build-docs
build-docs: docs/conf.py $(MARKDOWN) $(SRC)
	sphinx-build docs docs/_build/html

docs/resources/requirements.md: scripts/generate-requirements.md.sh requirements/*.txt
docs/resources/man.md: scripts/generate-man.md.sh $(MAN_DEPENDS)
docs/resources/translator.md: scripts/generate-translator.md.py $(SRC)
docs/resources/config.md: examples/config.py $(SRC)
docs/resources/vim.md: scripts/generate-vim.md.sh doc/*.txt
docs/misc/acknowledges.md: scripts/generate-acknowledges.md.sh $(SRC)
docs/misc/todo.md: scripts/generate-todo.md.sh $(SRC)
docs/api/%.md: scripts/generate-api.md.sh $(SRC)

addon-info.json: scripts/generate-addon-info.json.py pyproject.toml
	$(wordlist 1,2,$^) > $@

doc/%.txt: addon-info.json $(shell find . -type f -name '*.vim')
	pre-commit run vimdoc
# }}} build-docs #

# install {{{ #
.PHONY: install
install: install-man install-completions install-desktop-entry
	pip install -e .

.PHONY: install-man
dist/trans.1.gz: build
install-man: dist/trans.1.gz
	install -Dm644 $< $(MANPATH)

.PHONY: install-completions
install-completions: install-bash-completion install-zsh-completion install-tcsh-completion

.PHONY: install-bash-completion
dist/trans: build
install-bash-completion: dist/trans
	install -Dm644 $< $(BASH_COMPLETION)

.PHONY: install-zsh-completion
dist/_trans: build
install-zsh-completion: dist/_trans
	install -Dm644 $< $(ZSH_COMPLETION)

.PHONY: install-tcsh-completion
dist/trans.csh: build
install-tcsh-completion: dist/trans.csh
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
	rm -rf docs/_build $(GENERATE_MARKDOWN) $(_VERSION_PY) src/*.egg-info dist

.PHONY: test
test:
	$(THEMIS)
	pytest --cov
	pre-commit run -a

.PHONY: help
help:
	@cat docs/resources/make.md
# ex: foldmethod=marker
