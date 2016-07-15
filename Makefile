html:
	python3 pep2html.py


gh-pages: html
	ghp-import -n -m "Render PEPs" build/

.PHONY: html gh-pages
