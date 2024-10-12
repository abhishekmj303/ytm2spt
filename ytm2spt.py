# Nuitka Configuration
# nuitka-project: --enable-plugins=pyside6
# nuitka-project: --user-package-configuration-file=ytmusicapi.nuitka-package.config.yaml
#
# Compilation mode, standalone everywhere, except on macOS there app bundle
# nuitka-project-if: {OS} in ("Linux", "FreeBSD"):
#    nuitka-project: --onefile
# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --standalone
# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --standalone
#    nuitka-project: --macos-create-app-bundle
#
# Debugging options, controlled via environment variable at compile time.
# nuitka-project-if: os.getenv("DEBUG_COMPILATION", "yes") == "yes":
#     nuitka-project: --enable-console
# nuitka-project-else:
#     nuitka-project: --disable-console

from src.ytm2spt import main

main()
