# Build snellius-fs.pdf from snellius-fs.org.
# `make clean` removes the build files and keeps the PDF.
# Emacs exports the Org source, then tectonic compiles the deck.
# Needs Emacs with Org 9.6 or newer, tectonic, TikZ, varwidth,
# Carlito, Liberation Sans and Mono, DejaVu Sans, and TeX Gyre Cursor.

DECK := snellius-fs

all: $(DECK).pdf

$(DECK).tex: $(DECK).org export.el
	emacs --batch $(DECK).org --load export.el

$(DECK).pdf: $(DECK).tex pptx-style.tex $(DECK)-style.tex $(wildcard figures/*) $(wildcard figures/snellius-fs/*)
	tectonic -Z shell-escape-cwd=$(CURDIR) --keep-logs $(DECK).tex
	python3 deck-gate.py --pdf $(DECK).pdf --log $(DECK).log --allow deck-gate.allow $(if $(REFERENCE),--reference $(REFERENCE))

clean:
	latexmk -c $(DECK).tex
	-rm -f $(DECK).tex $(DECK).*vrb $(DECK).xdv $(DECK).nav $(DECK).snm

.PHONY: all clean
