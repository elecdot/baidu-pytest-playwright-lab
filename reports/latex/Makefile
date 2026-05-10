TEX = main.tex
PDF = main.pdf

.PHONY: pdf clean

pdf:
	latexmk -xelatex -interaction=nonstopmode -halt-on-error $(TEX)

clean:
	latexmk -C $(TEX)
	rm -f *.xdv
