# Build qcg-pilotjob-slides.pdf from qcg-pilotjob-slides.org.
# `make clean` removes the build files and keeps the PDF.
# Needs Emacs with Org 9.6 or newer, XeLaTeX, latexmk, TikZ, varwidth,
# Carlito, Liberation Sans and Mono, and DejaVu Sans.
# On Debian or Ubuntu:
#   apt install emacs-nox latexmk texlive-xetex texlive-latex-extra \
#     texlive-pictures fonts-crosextra-carlito fonts-liberation \
#     fonts-dejavu-core

DECK := qcg-pilotjob-slides

all: $(DECK).pdf

$(DECK).tex: $(DECK).org export.el
	emacs --batch $(DECK).org --load export.el

$(DECK).pdf: $(DECK).tex pptx-style.tex $(DECK)-style.tex $(wildcard figures/$(DECK)/*)
	latexmk -xelatex -interaction=nonstopmode -halt-on-error $(DECK).tex

clean:
	latexmk -c $(DECK).tex
	-rm -f $(DECK).tex $(DECK).*vrb $(DECK).xdv $(DECK).nav $(DECK).snm

.PHONY: all clean
