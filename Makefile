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
GENERATE_MARKDOWN = $(basename $(shell find docs -type f -name '*.md.in'))
MARKDOWN = README.md $(shell find docs -type f -name '*.md') $(GENERATE_MARKDOWN)
EXTERNAL_MAIN_PY = $(shell find $(LIBPATH)/external/* -name __main__.py)
EXTERNAL_INIT_PY = $(addsuffix __init__.py,$(dir $(EXTERNAL_MAIN_PY)))
_VERSION_PY = $(LIBPATH)/_version.py
GENERATE_PY = $(EXTERNAL_INIT_PY) $(_VERSION_PY)
SRC = $(shell find $(LIBPATH) -type f -name '*.py') \
			$(GENERATE_PY) \
			$(shell find $(LIBPATH)/assets -type f -name '*') \
			$(LIBPATH)/assets/txt/epilog.txt \
			$(LIBPATH)/assets/txt/version.txt \
			pyproject.toml
MAN_DEPENDS = scripts/$(BINNAME) $(SRC) addon-info.json
GITIGNORE_MARKDOWN = $(patsubst docs%,%,$(GENERATE_MARKDOWN))

.PHONY: default
default: install

.PHONY: all
all: test build build-docs doc/*.txt

.PHONY: build
build: dist/trans.1.gz dist/trans dist/_trans dist/trans.csh

.PHONY: install
install: install-bin install-man install-completions install-desktop-entry

.PHONY: install-bin
install-bin: $(SRC)
	pip install '.$(EXTRA)'

.PHONY: install-bin-editable
install-bin-editable: $(SRC)
	pip install -e '.$(EXTRA)'

%/_version.py:
	python -m build

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

dist/trans.1.gz: $(MAN_DEPENDS)
	mkdir -p $(dir $@)
	help2man $< | gzip > $@

dist/trans: $(SRC)
	mkdir -p $(dir $@)
	$(PRINT_COMPLETIONS) bash > $@

dist/_trans: $(SRC)
	mkdir -p $(dir $@)
	$(PRINT_COMPLETIONS) zsh > $@

dist/trans.csh: $(SRC)
	mkdir -p $(dir $@)
	$(PRINT_COMPLETIONS) tcsh > $@

.PHONY: install-man
install-man: dist/trans.1.gz
	install -Dm644 $< $(MANPATH)

.PHONY: install-completions
install-completions: install-bash-completion install-zsh-completion install-tcsh-completion

.PHONY: install-bash-completion
install-bash-completion: dist/trans
	install -Dm644 $< $(BASH_COMPLETION)

.PHONY: install-zsh-completion
install-zsh-completion: dist/_trans
	install -Dm644 $< $(ZSH_COMPLETION)

.PHONY: install-tcsh-completion
install-tcsh-completion: dist/trans.csh
	install -Dm644 $< $(TCSH_COMPLETION)

.PHONY: install-desktop-entry
install-desktop-entry: assets/desktop/*.desktop $(LIBPATH)/assets/images/icon.png
	install -D $< -t $(PREFIX)/share/applications
	install -D $(wordlist 2,2,$^) -t $(PREFIX)/share/$(LIBNAME)/images

.PHONY: uninstall
uninstall:
	rm -rf $(BASH_COMPLETION) $(ZSH_COMPLETION) $(TCSH_COMPLETION) $(MANPATH)
	pip uninstall $(LIBNAME)

.PHONY: build-docs
build-docs: docs/_build/html docs/.gitignore

docs/_build/html: docs/conf.py $(MARKDOWN) $(SRC)
	sphinx-build docs $@

%.md: scripts/eval-sh.pl %.md.in
	$(wordlist 1,2,$^) > $@

docs/resources/install.md: Makefile
docs/resources/requirements.md: scripts/generate-requirements.md.sh requirements/*.txt
docs/resources/man.md: scripts/generate-man.md.sh $(MAN_DEPENDS)
docs/resources/translator.md: scripts/generate-translator.md.py $(SRC)
docs/resources/config.md: examples/config.py $(SRC)
docs/resources/vim.md: scripts/generate-vim.md.sh doc/*.txt
docs/misc/%.md: $(SRC)
docs/api/%.md: scripts/generate-api.md.sh $(SRC)

docs/.gitignore:
	echo $(GITIGNORE_MARKDOWN) | perl -pe's/ /\n/g' > $@
	git rm -f --cached --ignore-unmatch $(GENERATE_MARKDOWN)

doc/%.txt: addon-info.json $(shell find . -type f -name '*.vim')
	vimdoc .

addon-info.json: scripts/generate-addon-info.json.py pyproject.toml
	$(wordlist 1,2,$^) > $@

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
