# shellcheck shell=bash
# $1=COMP_WORDS[1]
_shtab_greeter_compgen_PYFiles() {
	compgen -d -- "$1" # recurse into subdirs
	compgen -f -X '!*?.py' -- "$1"
	compgen -f -X '!*?.PY' -- "$1"
}
