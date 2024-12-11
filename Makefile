all:
	echo "Nothing to do"

.PHONY: images
images:
	cat images/filenames.txt | xargs -n 1 -I{} curl -O --output-dir images/ \
		-z 'images/{}' \
		--variable base=https://enos.itcollege.ee/~takraa/ics0026img/ \
		--expand-url '{{base}}/{}'

# TODO: figure out how to use wildacrd rules while keeping phonies

.PHONY: slides/00
slides/00:
	latexmk -lualatex -cd -c slides/00/00_handout.tex
	latexmk -lualatex -cd -c slides/00/00_presentation.tex

.PHONY: slides/01
slides/01:
	latexmk -lualatex -cd -c slides/01/01_handout.tex
	latexmk -lualatex -cd -c slides/01/01_presentation.tex

.PHONY: slides/02
slides/02:
	latexmk -lualatex -cd -c slides/02/02_handout.tex
	latexmk -lualatex -cd -c slides/02/02_presentation.tex

.PHONY: slides/03
slides/03:
	latexmk -lualatex -cd -c slides/03/03_handout.tex
	latexmk -lualatex -cd -c slides/03/03_presentation.tex

.PHONY: slides/04
slides/04:
	latexmk -lualatex -cd -c slides/04/04_handout.tex
	latexmk -lualatex -cd -c slides/04/04_presentation.tex

.PHONY: slides/05
slides/05:
	latexmk -lualatex -cd -c slides/05/05_handout.tex
	latexmk -lualatex -cd -c slides/05/05_presentation.tex

.PHONY: slides/06
slides/06:
	latexmk -lualatex -cd -c slides/06/06_handout.tex
	latexmk -lualatex -cd -c slides/06/06_presentation.tex

.PHONY: slides/07
slides/07:
	latexmk -lualatex -cd -c slides/07/07_handout.tex
	latexmk -lualatex -cd -c slides/07/07_presentation.tex

.PHONY: slides/08
slides/08:
	latexmk -lualatex -cd -c slides/08/08_handout.tex
	latexmk -lualatex -cd -c slides/08/08_presentation.tex

.PHONY: slides/09
slides/09:
	latexmk -lualatex -cd -c slides/09/09_handout.tex
	latexmk -lualatex -cd -c slides/09/09_presentation.tex

.PHONY: slides/10
slides/10:
	latexmk -lualatex -cd -c slides/10/10_handout.tex
	latexmk -lualatex -cd -c slides/10/10_presentation.tex

.PHONY: slides/11
slides/11:
	latexmk -lualatex -cd -c slides/11/11_handout.tex
	latexmk -lualatex -cd -c slides/11/11_presentation.tex

.PHONY: slides/12
slides/12:
	latexmk -lualatex -cd -c slides/12/12_handout.tex
	latexmk -lualatex -cd -c slides/12/12_presentation.tex

.PHONY: slides/13
slides/13:
	latexmk -lualatex -cd -c slides/13/13_handout.tex
	latexmk -lualatex -cd -c slides/13/13_presentation.tex

.PHONY: slides/14
slides/14:
	latexmk -lualatex -cd -c slides/14/14_handout.tex
	latexmk -lualatex -cd -c slides/14/14_presentation.tex

.PHONY: slides/15
slides/13:
	latexmk -lualatex -cd -c slides/15/15_handout.tex
	latexmk -lualatex -cd -c slides/15/15_presentation.tex