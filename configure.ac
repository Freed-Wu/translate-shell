#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.71])
m4_define([VERSION],
					m4_esyscmd([scripts/print-version.sh]))
AC_INIT([translate-shell],
				m4_defn([VERSION]),
				[https://github.com/Freed-Wu/translate-shell/issues],
				[translate-shell-]m4_defn([VERSION]),
				[https://github.com/Freed-Wu/translate-shell])
AC_CONFIG_AUX_DIR([build-aux])
AM_INIT_AUTOMAKE([subdir-objects -Wall -Werror foreign])
# cannot install python module which is a directory
# AM_PATH_PYTHON([3.6])

# Checks for programs.

# Checks for libraries.

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
