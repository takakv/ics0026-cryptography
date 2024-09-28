all:
	echo "Nothing to do"

.PHONY: images
images:
	cat images/filenames.txt | xargs -n 1 -I{} curl -O --output-dir images/ \
		-z 'images/{}' \
		--variable base=https://enos.itcollege.ee/~takraa/ics0026img/ \
		--expand-url '{{base}}/{}'
