# Makefile for fuzzer test application
#

# You can set these variables from the command line.
HCOMPILER     = ghc
COMPOPTS      = --make
BUILDDIR      = build

.PHONY: clean

testfuzz: testfuzz.hs
	$(HCOMPILER) $(COMPOPTS) testfuzz.hs

clean:
	rm -f *.hi *.o
