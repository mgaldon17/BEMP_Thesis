FILE := main
OUT  := build
NAME := BEMP_Thesis_of_Manuel_Galdon

.PHONY: pdf
pdf:
	latexmk -interaction=nonstopmode -outdir=$(OUT) -pdf -halt-on-error -jobname=$(NAME) $(FILE)
	cp -f $(OUT)/$(NAME).pdf $(NAME).pdf

.PHONY: watch
watch:
	latexmk -interaction=nonstopmode -outdir=$(OUT) -pdf -pvc -halt-on-error -jobname=$(NAME) $(FILE)

.PHONY: clean
clean:
	rm -rf $(filter-out $(OUT)/$(NAME).pdf, $(wildcard $(OUT)/*))

.PHONY: purge
purge:
	rm -rf $(OUT)
