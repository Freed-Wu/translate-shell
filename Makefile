PREFIX = /usr
BINNAME = trans
THEMIS = themis
LIBNAME = $(notdir $(CURDIR))
MANPATH = $(PREFIX)/share/man/man1/$(BINNAME).1.gz
PRINT_COMPLETIONS = $(BINNAME) --print-completion
BASH_COMPLETION = $(PREFIX)/share/bash-completion/completions/$(BINNAME)
ZSH_COMPLETION = $(PREFIX)/share/zsh/site-functions/_$(BINNAME)
TCSH_COMPLETION = /etc/profile.d/$(BINNAME).csh
GENERATE_MARKDOWN = $(basename $(shell find docs -name *.md.in))
MARKDOWN = README.md $(shell find docs -name *.md) $(GENERATE_MARKDOWN)
EXTERNAL_MAIN_PY = $(wildcard src/*/external/*/__main__.py)
EXTERNAL_INIT_PY = $(addsuffix __init__.py,$(dir $(EXTERNAL_MAIN_PY)))
_VERSION_PY = $(subst -,_,src/$(LIBNAME)/_version.py)
GENERATE_PY = $(EXTERNAL_INIT_PY) $(_VERSION_PY)
PY = $(shell find src -name *.py) $(GENERATE_PY)

.PHONY: default
default: install

.PHONY: all
all: test dist build-docs doc

.PHONY: install
install: install-bin install-man install-completions

.PHONY: install-bin
install-bin: $(PY)
	pip install '.$(EXTRA)'

.PHONY: install-bin-editable
install-bin-editable: $(PY)
	pip install -e '.$(EXTRA)'

%/_version.py:
	python -m build

dist: $(PY)
	python -m build

src/translate_shell/external/%/__init__.py: scripts/generate-__init__.py.py src/translate_shell/external/%/__main__.py templates/__init__.py
	$^ > $@

.PHONY: install-man
install-man: $(PY)
	help2man $(BINNAME) | gzip --stdout | sudo tee $(MANPATH) > /dev/null

.PHONY: install-completions
install-completions: install-bash-completion install-zsh-completion install-tcsh-completion

.PHONY: install-bash-completion
install-bash-completion: $(PY)
	$(PRINT_COMPLETIONS) bash | sudo tee $(BASH_COMPLETION) > /dev/null
.PHONY: install-zsh-completion
install-zsh-completion: $(PY)
	$(PRINT_COMPLETIONS) zsh | sudo tee $(ZSH_COMPLETION) > /dev/null
.PHONY: install-tcsh-completion
install-tcsh-completion: $(PY)
	$(PRINT_COMPLETIONS) tcsh | sudo tee $(TCSH_COMPLETION) > /dev/null

.PHONY: uninstall
uninstall:
	rm -rf $(BASH_COMPLETION) $(ZSH_COMPLETION) $(TCSH_COMPLETION) $(MANPATH)
	pip uninstall $(LIBNAME)

.PHONY: build-docs
build-docs: docs/_build/html docs/.gitignore

docs/_build/html: docs/conf.py $(MARKDOWN) $(PY)
	sphinx-build docs $@

%.md: scripts/eval-sh.pl %.md.in
	$(wordlist 1,2,$^) > $@

docs/resources/install.md: Makefile
docs/resources/requirements.md: requirements/*.txt
docs/resources/man.md: $(PY)
docs/resources/translator.md: $(PY)
docs/resources/config.md: examples/config.py $(PY)
docs/misc/%.md: $(PY)
docs/api/%.md: $(PY)

GITIGNORE_MARKDOWN = $(patsubst docs%,%,$(GENERATE_MARKDOWN))
docs/.gitignore:
	echo $(GITIGNORE_MARKDOWN) | perl -pe's/ /\n/g' > $@
	git rm --cached --ignore-unmatch $(GENERATE_MARKDOWN)

DOC_DEPENDS = addon-info.json $(shell find -name *.vim)
doc: $(DOC_DEPENDS)
	vimdoc .

addon-info.json: scripts/generate-addon-info.json.py pyproject.toml $(PY)
	$(wordlist 1,2,$^) > $@

.PHONY: clean
clean:
	rm -rf docs/_build docs/.gitignore $(GENERATE_MARKDOWN) $(GENERATE_PY) \
		src/*.egg-info dist addon-info.json

.PHONY: test
test: $(DOC_DEPENDS)
	$(THEMIS)
	pytest --cov
	pre-commit run

.PHONY: help
help:
	@cat docs/resources/make.md
