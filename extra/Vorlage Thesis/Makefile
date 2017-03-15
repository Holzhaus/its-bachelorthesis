COMMAND=latexmk -pdf
TEX=thesis
ALLTEX=$(wildcard *.tex)

OBJEXT=.aux ._aux .bbl .blg .glg .glo .gls .fls .idx .lof .log ._log .lol .out .pdfsync .toc .xdy .synctex.gz .vrb .cut .fdb_latexmk .loa .lot
OBJ=$(addprefix $(TEX), $(OBJEXT))

all: thesis
clean:
	@echo Cleaning all file with extension $(OBJEXT)
	$(foreach type,$(OBJEXT),$(shell find . -name '*$(type)' -exec echo rm -vf '{}' +))

cleanall: clean
	rm -f $(wildcard *.pdf)

thesis: $(TEX).pdf
$(TEX).pdf: $(TEX).tex $(ALLTEX)
	$(COMMAND) $(firstword $^)

