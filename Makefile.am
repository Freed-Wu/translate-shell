dist_doc_DATA = README.md
dist_man_MANS = sdist/trans.1
bashcompletiondir = $(datadir)/bash-completion/completions
dist_bashcompletion_DATA = sdist/trans
zshcompletiondir = $(datadir)/zsh/site-functions
dist_zshcompletion_DATA = sdist/_trans
desktopdir = $(datadir)/applications
dist_desktop_DATA = assets/desktop/translate-shell.desktop
icondir = $(datadir)/icons/hicolor/256x256/apps
dist_icon_DATA = src/translate_shell/assets/images/translate-shell.png

html-local:
	cd docs && sphinx-build -M html . _build
install-html-local: html-local
	install -d $(docdir)
	cp -r docs/_build/html $(docdir)

install-data-local:
	python -m installer -p $(DESTDIR)/$(prefix) dist/translate_shell-$(PACKAGE_VERSION)-py3-none-any.whl

check-local:
	cd src && python -m pytest ..

clean-local:
	rm -rf dist build src/translate_shell/_version.py src/translate_shell/_metainfo.py
