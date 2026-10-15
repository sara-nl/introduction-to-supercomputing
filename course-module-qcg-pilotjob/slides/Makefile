# Build qcg-pilotjob-slides.pdf and workflow-alternatives.pdf from their Org sources.
# Both decks share pptx-style.tex, export.el and the QCG deck's fonts and colours.
# `make clean` removes the build files and keeps the PDFs.
# Needs Emacs with Org 9.6 or newer, XeLaTeX, latexmk, TikZ, varwidth,
# Carlito, Liberation Sans and Mono, and DejaVu Sans.
# On Debian or Ubuntu:
#   apt install emacs-nox latexmk texlive-xetex texlive-latex-extra \
#     texlive-pictures fonts-crosextra-carlito fonts-liberation \
#     fonts-dejavu-core

DECKS := qcg-pilotjob-slides workflow-alternatives

all: $(DECKS:=.pdf)

%.tex: %.org export.el
	emacs --batch $< --load export.el

%.pdf: %.tex pptx-style.tex qcg-pilotjob-slides-style.tex $(wildcard figures/*/*)
	latexmk -xelatex -interaction=nonstopmode -halt-on-error $<

clean:
	for d in $(DECKS); do latexmk -c $$d.tex; rm -f $$d.tex $$d.*vrb $$d.xdv $$d.nav $$d.snm; done

.PHONY: all clean
