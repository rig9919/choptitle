PYTHON=python
INSTALL=/usr/bin/install

BINDIR=/usr/local/bin
BUILDDIR=./build
MANDIR=/usr/local/share/man/man1
DISTPKGS=$(shell python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')
VERSION=$(shell git describe --tags --long)

all:
		cd ./src/py-phash && $(PYTHON) ./setup.py build
		mkdir $(BUILDDIR)
		cp ./src/findscreen $(BUILDDIR)/findscreen
		cp ./src/choptitle $(BUILDDIR)/choptitle
		sed -i "s/__version__ = \"git\"/__version__ = \"$(VERSION)\"/" $(BUILDDIR)/findscreen
		sed -i "s/__version__ = \"git\"/__version__ = \"$(VERSION)\"/" $(BUILDDIR)/choptitle

install:
		$(INSTALL) $(BUILDDIR)/findscreen $(BINDIR)/findscreen
		$(INSTALL) $(BUILDDIR)/choptitle $(BINDIR)/choptitle
		$(INSTALL) ./src/py-phash/build/lib.*/PypHash.so $(DISTPKGS)/PypHash.so

uninstall:
		rm -rf $(BINDIR)/findscreen
		rm -rf $(BINDIR)/choptitle
		rm -rf $(DISTPKGS)/PypHash.so
        
