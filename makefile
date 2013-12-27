PYTHON=python
INSTALL=/usr/bin/install

BINDIR=/usr/local/bin
MANDIR=/usr/local/share/man/man1
DISTPKGS=$(shell python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')

all:
		cd ./src/py-phash && $(PYTHON) ./setup.py build

install:
		$(INSTALL) ./src/findscreen $(BINDIR)/findscreen
		$(INSTALL) ./src/choptitle $(BINDIR)/choptitle
		$(INSTALL) ./src/py-phash/build/lib.*/PypHash.so $(DISTPKGS)/PypHash.so

uninstall:
		rm -rf $(BINDIR)/findscreen
		rm -rf $(BINDIR)/choptitle
		rm -rf $(DISTPKGS)/PypHash.so
        
