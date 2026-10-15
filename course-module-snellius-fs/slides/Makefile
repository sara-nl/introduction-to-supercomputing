# Build snellius-fs.pdf from snellius-fs.org.
# `make clean` removes the build files and keeps the PDF.
# Needs Emacs with Org 9.6 or newer, XeLaTeX, latexmk, the metropolis
# beamer theme, Fira Sans, Latin Modern Mono and TeX Gyre Cursor.
# On Debian or Ubuntu:
#   apt install emacs-nox latexmk texlive-xetex texlive-latex-extra \
#     texlive-pictures texlive-plain-generic texlive-fonts-recommended \
#     fonts-lmodern tex-gyre
# Fira Sans must be installed so that XeLaTeX finds it by name,
# for example from https://github.com/mozilla/Fira.

DECK := snellius-fs

all: $(DECK).pdf

$(DECK).tex: $(DECK).org export.el
	emacs --batch $(DECK).org --load export.el

$(DECK).pdf: $(DECK).tex surf-style.tex figures/*
	latexmk -xelatex -interaction=nonstopmode -halt-on-error $(DECK).tex

clean:
	latexmk -c $(DECK).tex
	-rm -f $(DECK).tex $(DECK).*vrb $(DECK).xdv $(DECK).nav $(DECK).snm

.PHONY: all clean
