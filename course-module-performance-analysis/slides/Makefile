# Build ../performance-analysis.pdf from performance-analysis.org.
# The PDF stays where the course links to it, one level up.
# `make clean` removes the build files and keeps the PDF.
# Needs Emacs with Org 9.6 or newer, XeLaTeX, latexmk, TikZ, varwidth,
# Roboto, Carlito, Liberation Sans and Mono, and Latin Modern Math.
# Aptos replaces Roboto when it is installed.
# On Debian or Ubuntu:
#   apt install emacs-nox latexmk texlive-xetex texlive-latex-extra \
#     texlive-pictures fonts-roboto-unhinted fonts-crosextra-carlito \
#     fonts-liberation fonts-lmodern

DECK := performance-analysis

all: ../$(DECK).pdf

$(DECK).tex: $(DECK).org export.el
	emacs --batch $(DECK).org --load export.el

$(DECK).pdf: $(DECK).tex pptx-style.tex $(DECK)-style.tex $(wildcard figures/$(DECK)/*)
	latexmk -xelatex -interaction=nonstopmode -halt-on-error $(DECK).tex

../$(DECK).pdf: $(DECK).pdf
	cp $(DECK).pdf ../$(DECK).pdf

clean:
	latexmk -c $(DECK).tex
	-rm -f $(DECK).tex $(DECK).pdf $(DECK).*vrb $(DECK).xdv $(DECK).nav $(DECK).snm

.PHONY: all clean
